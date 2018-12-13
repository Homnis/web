# Generated by Django 2.1.2 on 2018-11-13 02:25

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='books',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type_id', models.IntegerField(default=5, verbose_name='商品种类')),
                ('name', models.CharField(max_length=20, verbose_name='商品名称')),
                ('desc', models.CharField(max_length=128, verbose_name='商品简介')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品价格')),
                ('stock', models.IntegerField(default=1, verbose_name='商品库存')),
                ('sales', models.IntegerField(default=0, verbose_name='商品销量')),
                ('detail', tinymce.models.HTMLField(verbose_name='商品详情')),
                ('image', models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='E:\\web\\myStore\\static'), upload_to='books', verbose_name='商品图片')),
                ('status', models.IntegerField(default=1, verbose_name='商品状态')),
            ],
            options={
                'db_table': 's_books',
            },
        ),
        migrations.CreateModel(
            name='BooksImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='E:\\web\\myStore\\static'), upload_to='books', verbose_name='商品图片')),
                ('status', models.BooleanField(default=False, verbose_name='是否默认显示该图片')),
                ('books', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.books', verbose_name='所属商品')),
            ],
            options={
                'db_table': 'books_img',
            },
        ),
    ]
