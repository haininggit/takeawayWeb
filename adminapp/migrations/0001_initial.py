# Generated by Django 3.2 on 2021-05-05 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('status', models.IntegerField()),
                ('add_time', models.DateField()),
            ],
            options={
                'db_table': 'admin',
            },
        ),
    ]
