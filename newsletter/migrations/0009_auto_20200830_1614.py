# Generated by Django 3.0.8 on 2020-08-30 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0008_auto_20200830_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='status',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False')], max_length=10),
        ),
    ]
