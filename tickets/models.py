from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.crypto import get_random_string

from ironcage.utils import Scrambler

from .constants import DAYS
from . import prices

CHANGEABLE_REASONS = [
    'Django Girls',
    'Financial Assistance',
    'Conference Guest',
    'John Pinner Award 2017',
]


class Ticket(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    rate = models.CharField(max_length=40)
    sat = models.BooleanField()
    sun = models.BooleanField()
    mon = models.BooleanField()
    tue = models.BooleanField()
    wed = models.BooleanField()
    order_rows = GenericRelation('orders.OrderRow')
    free_reason = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    id_scrambler = Scrambler(2000)

    class Meta:
        permissions = [
            ('create_free_ticket', 'Can create free tickets'),
        ]

    class Manager(models.Manager):
        def get_by_ticket_id_or_404(self, ticket_id):
            id = self.model.id_scrambler.backward(ticket_id)
            return get_object_or_404(self.model, pk=id)

        def build(self, rate, days, owner=None, email_addr=None):
            assert bool(owner) ^ bool(email_addr)
            day_fields = {day: (day in days) for day in DAYS}
            ticket = self.model(rate=rate, owner=owner, **day_fields)

            if email_addr is not None:
                ticket.email_addr = email_addr

            return ticket

        def create_free_with_invitation(self, email_addr, free_reason, days=None):
            if days is None:
                days = {day: False for day in DAYS}
            else:
                days = {day: (day in days) for day in DAYS}
            ticket = self.create(free_reason=free_reason, **days)
            ticket.invitations.create(email_addr=email_addr)
            return ticket

    objects = Manager()

    def __str__(self):
        return self.ticket_id or 'Unsaved'

    @property
    def ticket_id(self):
        if self.id is None:
            return None
        return self.id_scrambler.forward(self.id)

    def save(self, **kwargs):
        super().save(**kwargs)
        if hasattr(self, 'email_addr'):
            self.invitations.create(email_addr=self.email_addr)

    def get_absolute_url(self):
        return reverse('tickets:ticket', args=[self.ticket_id])

    def days(self):
        return [DAYS[day] for day in DAYS if getattr(self, day)]

    def num_days(self):
        return len(self.days())

    def ticket_holder_name(self):
        # TODO this is a mess
        if self.owner:
            return self.owner.name
        elif self.pk:
            return self.invitation().email_addr
        else:
            return self.email_addr

    def order_company_name(self):
        if self.rate == 'corporate' and self.order:
            return self.order.billing_name
        return ''

    @property
    def descr_for_order(self):
        return f'{self.num_days()}-day {self.rate}-rate ticket'

    @property
    def descr_extra_for_order(self):
        return self.days_sentence

    @property
    def days_sentence(self):
        return ', '.join(self.days())

    @property
    def is_saved(self):
        return self.pk is not None

    @property
    def order_row(self):
        # We expect there to only ever be a single OrderRow, so this should never fail
        return self.order_rows.get()

    @property
    def order(self):
        if self.is_saved and not self.free_reason:
            return self.order_row.order
        else:
            return None

    @property
    def cost_excl_vat(self):
        if self.free_reason:
            return 0
        elif self.is_saved:
            return self.order_row.cost_excl_vat
        else:
            return prices.cost_excl_vat(self.rate, self.num_days())

    @property
    def cost_incl_vat(self):
        return int(self.cost_excl_vat * 1.2)

    def invitation(self):
        # This will raise an exception if a ticket has multiple invitations
        return self.invitations.get()

    def update_days(self, days):
        if self.is_changeable or len(self.days()) == 0:
            for day in DAYS:
                setattr(self, day, (day in days))
            self.save()

    @property
    def is_free_ticket(self):
        return self.free_reason is not None

    @property
    def is_changeable(self):
        return self.free_reason in CHANGEABLE_REASONS


class TicketInvitation(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='invitations', on_delete=models.CASCADE)  # TODO make this a OneToOneField
    email_addr = models.EmailField()
    name = models.CharField(max_length=100)
    token = models.CharField(max_length=24, unique=True)  # An index is automatically created since unique=True
    status = models.CharField(max_length=10, default='unclaimed')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Manager(models.Manager):
        def create(self, **kwargs):
            token = get_random_string(length=24)
            return super().create(token=token, **kwargs)

    objects = Manager()

    def get_absolute_url(self):
        return reverse('tickets:ticket_invitation', args=[self.token])

    def claim_for_owner(self, owner):
        # This would fail if owner already has a ticket, as Ticket.owner is a
        # OneToOneField.
        assert self.status == 'unclaimed'
        ticket = self.ticket
        ticket.owner = owner
        ticket.save()
        self.status = 'claimed'
        self.save()
