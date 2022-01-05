# Generated by Django 4.0 on 2022-01-05 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_product_category_alter_product_created_by'),
        ('cart', '0004_alter_orderitem_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='store.product'),
        ),
    ]
