# Generated by Django 2.1.2 on 2018-10-30 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_auto_20181030_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='avatar',
            field=models.ImageField(default='static/article/img/default.gif', upload_to='article/static/img/', verbose_name='用户头像'),
        ),
    ]
