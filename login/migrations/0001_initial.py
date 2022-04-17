# Generated by Django 4.0.3 on 2022-04-04 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deparment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=16, null=True, verbose_name='部门')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('password', models.CharField(max_length=64)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('account', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('creat_time', models.DateTimeField(blank=True, null=True, verbose_name='创建时间')),
                ('gender', models.SmallIntegerField(blank=True, choices=[(0, '男'), (1, '女')], null=True, verbose_name='性别')),
                ('deparment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='login.deparment')),
            ],
        ),
    ]