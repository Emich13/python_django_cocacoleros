# Generated by Django 4.0.1 on 2022-01-17 23:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UserApp', '0005_remove_post_tematica_post_tematica'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentariospost',
            name='comentarista',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='post',
            name='tematica',
        ),
        migrations.AddField(
            model_name='post',
            name='tematica',
            field=models.ManyToManyField(to='UserApp.Tematica'),
        ),
        migrations.CreateModel(
            name='Favoritos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserApp.post')),
            ],
        ),
    ]
