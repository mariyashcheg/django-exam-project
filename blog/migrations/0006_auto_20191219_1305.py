# Generated by Django 2.2.6 on 2019-12-19 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20191219_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(default='http://placehold.it/500x325', upload_to='blog/static/blog/img'),
        ),
    ]