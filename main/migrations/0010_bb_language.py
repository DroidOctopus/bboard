# Generated by Django 4.0.4 on 2022-08-04 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_comment_author_en_remove_comment_author_uk_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bb',
            name='language',
            field=models.CharField(default='uk', max_length=2, null=True, verbose_name='Мова оголошення'),
        ),
    ]
