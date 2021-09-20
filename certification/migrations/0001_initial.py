# Generated by Django 3.2.4 on 2021-09-20 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authenticate', '0002_university'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('certificate_id', models.AutoField(primary_key=True, serialize=False)),
                ('course', models.CharField(max_length=32)),
                ('grade_obtained', models.CharField(max_length=3)),
                ('certified_on', models.DateField(null=True)),
                ('certificate_link', models.CharField(max_length=128, null=True)),
                ('certified', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authenticate.student')),
                ('university', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='authenticate.university')),
            ],
        ),
    ]