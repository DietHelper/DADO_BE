# Generated by Django 4.2.7 on 2024-03-02 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profileImage',
        ),
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
