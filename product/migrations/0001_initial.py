# Generated by Django 3.0.4 on 2020-04-03 04:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='product_category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100, verbose_name='Category')),
            ],
        ),
        migrations.CreateModel(
            name='product_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(verbose_name='Description')),
                ('rent_rate', models.IntegerField(verbose_name='Rent')),
                ('deposit', models.IntegerField(default=0, verbose_name='Deposit')),
                ('upload_time', models.DateTimeField(auto_now_add=True, verbose_name='Uploaded at')),
                ('last_edit_time', models.DateTimeField(auto_now=True, verbose_name='Last edit')),
                ('publish', models.BooleanField(default=False)),
                ('condition', models.TextField(verbose_name='Terms and Conditions')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.product_category')),
            ],
        ),
        migrations.CreateModel(
            name='product_rent_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rent_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='product_question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=100)),
                ('question_time', models.DateTimeField(auto_now_add=True)),
                ('last_edit_time', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product_details')),
                ('who_is_asking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='product_profile_img',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_profile_img', models.ImageField(upload_to='pics/add_product/product_img', verbose_name='Product Profile Image')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='product.product_details')),
            ],
        ),
        migrations.CreateModel(
            name='product_img',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_img', models.ImageField(upload_to='pics/add_product/product_img', verbose_name='Product Image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product_details')),
            ],
        ),
        migrations.AddField(
            model_name='product_details',
            name='rent_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.product_rent_type'),
        ),
        migrations.AddField(
            model_name='product_details',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='product_available_location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=15, max_digits=20)),
                ('longitude', models.DecimalField(decimal_places=15, max_digits=20)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='product.product_details')),
            ],
        ),
        migrations.CreateModel(
            name='answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=255)),
                ('answer_time', models.DateTimeField(auto_now_add=True)),
                ('last_edit_time', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product_question')),
            ],
        ),
    ]