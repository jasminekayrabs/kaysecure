# Generated by Django 5.0.4 on 2024-05-17 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_rename_is_completed_usermoduleprogress_completed_module_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='slide',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='slide',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
