# Generated by Django 4.0.1 on 2022-02-09 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default='defaultemail@test.com', max_length=254, unique=True),
        ),
    ]
