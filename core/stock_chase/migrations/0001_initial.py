# Generated by Django 4.0.4 on 2022-05-15 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProdcutListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_channel', models.CharField(choices=[('trendyol', 'Trendyol'), ('hepsiburada', 'Hepsiburada')], max_length=50)),
                ('name', models.CharField(max_length=250)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('stock_code', models.CharField(max_length=25)),
                ('is_bundle', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=True, help_text='Active products will show in selling list', verbose_name='is active?')),
            ],
            options={
                'verbose_name_plural': 'Products List',
            },
        ),
        migrations.CreateModel(
            name='ProductGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('bundle_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group', to='stock_chase.prodcutlisting')),
            ],
            options={
                'verbose_name_plural': 'Product Group',
            },
        ),
    ]
