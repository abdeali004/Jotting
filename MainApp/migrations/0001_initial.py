# Generated by Django 3.1.2 on 2020-12-06 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='userInfo',
            fields=[
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('newUser', models.BooleanField(default=True)),
                ('checkCode', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.TextField()),
                ('main_note', models.TextField(default='')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
