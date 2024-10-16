# Generated by Django 5.1.1 on 2024-09-25 17:10

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('created_when', models.DateTimeField(auto_now_add=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='question',
            name='passage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='Core.passage'),
        ),
    ]