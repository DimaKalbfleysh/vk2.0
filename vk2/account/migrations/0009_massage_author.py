# Generated by Django 2.1.5 on 2019-02-12 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_dialog_id_dialog'),
    ]

    operations = [
        migrations.AddField(
            model_name='massage',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='massages', to='account.Account'),
        ),
    ]
