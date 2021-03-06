# Generated by Django 4.0.1 on 2022-02-16 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accommodation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=250)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('address', models.CharField(max_length=250)),
                ('region', models.CharField(max_length=30)),
                ('is_verified', models.BooleanField(default=False)),
                ('latitude', models.DecimalField(decimal_places=7, max_digits=10)),
                ('longtitude', models.DecimalField(decimal_places=7, max_digits=10)),
                ('check_in_time', models.DateTimeField()),
                ('check_out_time', models.DateTimeField()),
                ('minimum_stay', models.PositiveIntegerField(default=1)),
            ],
            options={
                'db_table': 'accommodations',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment', models.CharField(max_length=250)),
                ('score', models.PositiveIntegerField()),
                ('accommodation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accommodations.accommodation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'reviews',
            },
        ),
        migrations.CreateModel(
            name='ThemaGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('accommodation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accommodations.accommodation')),
            ],
            options={
                'db_table': 'thema_groups',
            },
        ),
        migrations.CreateModel(
            name='ReviewImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image_url', models.CharField(max_length=250)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accommodations.review')),
            ],
            options={
                'db_table': 'review_images',
            },
        ),
        migrations.CreateModel(
            name='AccommodationImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image_url', models.CharField(max_length=250)),
                ('accommodation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accommodations.accommodation')),
            ],
            options={
                'db_table': 'accommodation_images',
            },
        ),
    ]
