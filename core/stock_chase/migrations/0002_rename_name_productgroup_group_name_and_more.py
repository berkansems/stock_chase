# Generated by Django 4.0.4 on 2022-05-15 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_chase', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productgroup',
            old_name='name',
            new_name='group_name',
        ),
        migrations.AlterField(
            model_name='prodcutlisting',
            name='sales_channel',
            field=models.CharField(choices=[('trendyol', 'Trendyol'), ('hepsiburada', 'Hepsiburada')], db_index=True, max_length=50),
        ),
    ]
