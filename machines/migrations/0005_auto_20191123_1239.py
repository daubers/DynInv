# Generated by Django 2.2.7 on 2019-11-23 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0004_auto_20191123_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupvars',
            name='vault_path',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hostvars',
            name='vault_path',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
