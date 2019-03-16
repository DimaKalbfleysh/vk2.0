# Generated by Django 2.1.5 on 2019-03-01 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0026_auto_20190226_0014'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True)),
                ('status', models.CharField(max_length=150, null=True)),
                ('description', models.CharField(max_length=450, null=True)),
                ('web_site', models.CharField(max_length=150, null=True)),
                ('main_photo', models.ImageField(blank=True, default='defult-photo.png', null=True, upload_to='')),
                ('header_photo', models.ImageField(blank=True, default=None, null=True, upload_to='')),
                ('user', models.ManyToManyField(blank=True, null=True, related_name='group', to='account.Account')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='account.Group'),
        ),
    ]