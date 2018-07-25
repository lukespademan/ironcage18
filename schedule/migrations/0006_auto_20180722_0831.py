# Generated by Django 2.0.3 on 2018-07-22 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_auto_20180722_0826'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='accessibility_notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='accessible_auditorium',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='room',
            name='accessible_stage',
            field=models.BooleanField(),
        ),
    ]