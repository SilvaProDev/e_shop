# Generated by Django 3.0.8 on 2020-09-02 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0009_auto_20200830_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='status',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False')], max_length=10),
        ),
    ]
