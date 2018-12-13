# Generated by Django 2.1.2 on 2018-10-26 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('psw', models.CharField(max_length=20)),
                ('gender', models.CharField(max_length=5)),
                ('age', models.IntegerField()),
                ('address', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]