# Generated by Django 3.2.4 on 2021-10-20 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scaffolding', '0003_coursedetails_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursedetails',
            name='status',
            field=models.CharField(default='COMPLETE', max_length=32),
        ),
    ]
