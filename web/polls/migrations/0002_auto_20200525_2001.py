# Generated by Django 3.0.6 on 2020-05-25 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='question',
            new_name='question_text',
        ),
        migrations.AddField(
            model_name='question',
            name='publish_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date published'),
        ),
    ]
