# Generated by Django 2.0 on 2018-11-14 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_auto_20181114_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Books', verbose_name='书籍'),
        ),
    ]