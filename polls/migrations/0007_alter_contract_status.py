# Generated by Django 4.2.1 on 2023-06-05 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_alter_contract_agent_alter_contract_client_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='status',
            field=models.CharField(blank=True, choices=[('PENDING', 'Pending'), ('ACTIVE', 'Active'), ('OUTDATED', 'Outdated'), ('DECLINED', 'Declined')], default='PENDING', max_length=15, null=True),
        ),
    ]
