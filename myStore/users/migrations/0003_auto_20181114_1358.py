# Generated by Django 2.0 on 2018-11-14 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20181114_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passport',
            name='email',
            field=models.EmailField(default='', max_length=254, verbose_name='用户邮箱'),
        ),
        migrations.AlterField(
            model_name='passport',
            name='tel',
            field=models.CharField(default='', max_length=11, verbose_name='电话'),
        ),
    ]
