# Generated by Django 2.2.16 on 2022-12-03 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': ('Отзыв',), 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.RenameField(
            model_name='review',
            old_name='scope',
            new_name='score',
        ),
    ]