# Generated by Django 4.0.4 on 2022-08-04 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_bb_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bb',
            name='language',
            field=models.CharField(default='uk', max_length=5, verbose_name='Мова оголошення'),
        ),
    ]