# Generated by Django 5.0.5 on 2024-05-09 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comments", "0002_alter_comment_reply_to_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commentattachment",
            name="file",
            field=models.FileField(upload_to="files/attachments/"),
        ),
    ]
