# Generated by Django 4.0 on 2022-03-03 14:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('username', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Username')),
                ('full_name', models.CharField(max_length=50, verbose_name='Full Name')),
                ('dob', models.DateField(verbose_name='Date of birth')),
                ('user_type', models.CharField(choices=[('P', 'Patient'), ('H', 'Hospital'), ('D', 'Doctor')], max_length=2)),
                ('image', models.ImageField(blank=True, null=True, upload_to='userprofile')),
                ('phone', models.CharField(blank=True, max_length=10)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
