# Generated by Django 2.1.5 on 2019-03-27 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True)),
                ('status', models.CharField(blank=True, max_length=150, null=True)),
                ('description', models.CharField(blank=True, max_length=450, null=True)),
                ('web_site', models.CharField(blank=True, max_length=150, null=True)),
                ('main_photo', models.ImageField(blank=True, default='defult-photo.png', null=True, upload_to='')),
                ('header_photo', models.ImageField(blank=True, default=None, null=True, upload_to='')),
                ('number_subscribers', models.IntegerField(default=0, null=True)),
                ('admin', models.ManyToManyField(related_name='group_for_admin', to='account.Account')),
            ],
        ),
    ]
