# Generated by Django 5.1.1 on 2024-09-27 15:34

import ckeditor.fields
import django.utils.timezone
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0004_alter_passage_category_alter_passage_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='explanation',
            field=ckeditor.fields.RichTextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]