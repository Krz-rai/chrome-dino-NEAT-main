# Generated by Django 5.1.1 on 2024-09-30 17:47

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0007_quizattempt_questionresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passage',
            name='text',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
