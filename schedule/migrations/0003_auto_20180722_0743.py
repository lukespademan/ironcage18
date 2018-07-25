# Generated by Django 2.0.3 on 2018-07-22 07:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_auto_20180722_0742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='additional_people',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='session',
            name='chair',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chaired_sessions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='session',
            name='length',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stream',
            name='day',
            field=models.CharField(choices=[('mon', 'Monday'), ('sun', 'Sunday'), ('wed', 'Wednesday'), ('tue', 'Tuesday'), ('sat', 'Saturday')], max_length=3),
        ),
    ]