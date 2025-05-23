# Generated by Django 4.2.2 on 2023-07-19 15:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academy', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='progress',
            name='enroled_courses',
            field=models.ManyToManyField(related_name='enroled_courses', to='academy.course'),
        ),
        migrations.AddField(
            model_name='progress',
            name='finished_courses',
            field=models.ManyToManyField(related_name='finished_courses', to='academy.course'),
        ),
        migrations.AddField(
            model_name='progress',
            name='finished_lessons',
            field=models.ManyToManyField(to='academy.lesson'),
        ),
        migrations.AddField(
            model_name='progress',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lesson',
            name='chapter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='academy.chapter'),
        ),
        migrations.AddField(
            model_name='course',
            name='role',
            field=models.ManyToManyField(to='users.role'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='academy.course'),
        ),
    ]
