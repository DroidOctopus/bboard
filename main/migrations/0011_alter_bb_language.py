# Generated by Django 4.0.4 on 2022-08-04 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_bb_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bb',
            name='language',
            field=models.CharField(db_index=True, default='uk', max_length=2, null=True, verbose_name='Мова оголошення'),
        ),
    ]
