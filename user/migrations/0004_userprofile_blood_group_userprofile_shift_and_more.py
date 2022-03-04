# Generated by Django 4.0 on 2022-03-03 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_userprofile_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='blood_group',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='shift',
            field=models.CharField(blank=True, choices=[('M', 'Morning'), ('E', 'Evening')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(choices=[('P', 'Patient'), ('D', 'Doctor')], max_length=2),
        ),
    ]
