# Generated by Django 4.0.4 on 2022-04-20 06:40

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=255)),
                ('lname', models.CharField(max_length=255)),
                ('newsletters', models.BooleanField(default=True)),
                ('subscriptions', models.BooleanField(default=True)),
                ('username', models.CharField(max_length=40, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
                ('author', models.CharField(max_length=255)),
                ('ISBN', models.IntegerField(unique=True)),
                ('title', models.CharField(max_length=255)),
                ('genre', models.CharField(max_length=255)),
                ('numSold', models.IntegerField(default=0)),
                ('picture', models.CharField(blank=True, max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('in_stock', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Books',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=255)),
                ('lname', models.CharField(max_length=255)),
                ('newsletters', models.BooleanField(default=True)),
                ('subscriptions', models.BooleanField(default=True)),
                ('username', models.CharField(max_length=40, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('organizationName', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NewsLetter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emailTitle', models.CharField(max_length=255)),
                ('content', models.CharField(max_length=255)),
                ('scheduledTime', models.DateField()),
                ('attachment', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('startdate', models.DateField()),
                ('enddate', models.DateField()),
                ('code', models.CharField(max_length=24, unique=True)),
                ('pctdiscount', models.IntegerField(blank=True, max_length=4, null=True)),
                ('amountdiscount', models.IntegerField(blank=True, max_length=6, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('orderID', models.AutoField(primary_key=True, serialize=False)),
                ('purchaser', models.CharField(max_length=255)),
                ('totalPrice', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=255)),
                ('lname', models.CharField(max_length=255)),
                ('newsletters', models.BooleanField(default=True)),
                ('subscriptions', models.BooleanField(default=True)),
                ('username', models.CharField(max_length=40, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('birthDate', models.DateField()),
                ('phone', models.IntegerField(blank=True, max_length=10, null=True)),
                ('address', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=255)),
                ('lname', models.CharField(max_length=255)),
                ('newsletters', models.BooleanField(default=True)),
                ('subscriptions', models.BooleanField(default=True)),
                ('username', models.CharField(max_length=40, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BookSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salePrice', models.IntegerField()),
                ('saleDate', models.DateField(default=datetime.date(2022, 4, 20))),
                ('bookID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookID', to='website.book')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_creator', to='website.vendor'),
        ),
    ]
