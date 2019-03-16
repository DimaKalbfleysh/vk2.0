# Generated by Django 2.1.5 on 2019-03-13 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0049_auto_20190314_0102'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='birth_day',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31)], default='1', null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='month_birth',
            field=models.CharField(choices=[('Января', 'Января'), ('Февраля', 'Февраля'), ('Марта', 'Марта'), ('Апреля', 'Апреля'), ('Мая', 'Мая'), ('Июня', 'Июня'), ('Июля', 'Июля'), ('Августа', 'Августа'), ('Сентября', 'Сентября'), ('Октября', 'Октября'), ('Ноября', 'Ноября'), ('Декабря', 'Декабря')], default='Января', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='year_birth',
            field=models.IntegerField(choices=[(2005, 2005), (2004, 2004), (2003, 2003), (2002, 2002), (2001, 2001), (2000, 2000), (1999, 1999), (1998, 1998), (1997, 1997), (1996, 1996), (1995, 1995), (1994, 1994), (1993, 1993), (1992, 1992), (1991, 1991), (1990, 1990), (1989, 1989), (1988, 1988), (1987, 1987), (1986, 1986), (1985, 1985), (1984, 1984), (1983, 1983), (1982, 1982), (1981, 1981), (1980, 1980), (1979, 1979), (1978, 1978), (1977, 1977), (1976, 1976), (1975, 1975)], default='2005', null=True),
        ),
    ]