# Generated by Django 2.0.3 on 2018-04-08 15:57

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import orders.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billing_name', models.CharField(max_length=200, null=True)),
                ('billing_addr', models.TextField(null=True)),
                ('invoice_number', models.IntegerField(null=True, unique=True)),
                ('status', models.CharField(max_length=10)),
                ('stripe_charge_id', models.CharField(max_length=80)),
                ('stripe_charge_created', models.DateTimeField(null=True)),
                ('stripe_charge_failure_reason', models.CharField(blank=True, max_length=400)),
                ('unconfirmed_details', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('purchaser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, orders.models.SalesRecord),
        ),
        migrations.CreateModel(
            name='OrderRow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost_excl_vat', models.IntegerField()),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('item_descr', models.CharField(max_length=400)),
                ('item_descr_extra', models.CharField(max_length=400, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='contenttypes.ContentType')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_rows', to='orders.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=400)),
                ('credit_note_number', models.IntegerField()),
                ('stripe_refund_id', models.CharField(max_length=80)),
                ('stripe_refund_created', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            bases=(models.Model, orders.models.SalesRecord),
        ),
        migrations.AddField(
            model_name='orderrow',
            name='refund',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='order_rows', to='orders.Refund'),
        ),
    ]