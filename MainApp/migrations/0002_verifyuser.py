# Generated by Django 3.1.2 on 2020-12-07 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='verifyUser',
            fields=[
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=100)),
                ('verificationCode', models.CharField(max_length=12)),
            ],
        ),
    ]
