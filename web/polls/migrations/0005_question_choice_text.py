# Generated by Django 3.0.6 on 2020-05-25 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20200525_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='choice_text',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
