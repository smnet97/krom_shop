# Generated by Django 3.2.7 on 2021-09-17 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_cartmodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartmodel',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.productmodel'),
        ),
    ]