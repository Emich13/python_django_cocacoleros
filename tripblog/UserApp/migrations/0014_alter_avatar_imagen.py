# Generated by Django 4.0.1 on 2022-02-07 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0013_alter_post_imagenpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='imagen',
            field=models.ImageField(blank=True, default='profileImage.jpg', null=True, upload_to='avatares'),
        ),
    ]
