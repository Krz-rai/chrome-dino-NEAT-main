# Generated by Django 5.1.1 on 2024-09-27 17:44

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0005_alter_question_explanation'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='hint1',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='hint2',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='hint3',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]