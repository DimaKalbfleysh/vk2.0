# Generated by Django 2.1.5 on 2019-03-11 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0041_auto_20190311_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dialog',
            name='id_dialog',
            field=models.IntegerField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='dialog',
            name='number_not_read_messages',
            field=models.IntegerField(null=True),
        ),
    ]