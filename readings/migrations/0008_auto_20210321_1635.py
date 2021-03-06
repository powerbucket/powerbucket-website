# Generated by Django 3.1.5 on 2021-03-21 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readings', '0007_auto_20210221_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='calculate_online',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='reading',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='settings',
            name='r',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='settings',
            name='update',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='settings',
            name='x',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='settings',
            name='y',
            field=models.IntegerField(default=0),
        ),
    ]
