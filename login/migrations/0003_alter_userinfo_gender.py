# Generated by Django 4.0.3 on 2022-04-08 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_alter_deparment_title_alter_userinfo_account_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='gender',
            field=models.SmallIntegerField(choices=[(0, '男'), (1, '女')], default=0, verbose_name='性别'),
        ),
    ]
