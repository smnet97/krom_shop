# Generated by Django 3.2.7 on 2021-09-11 11:11

from django.db import migrations, models
import krom.validators


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(db_index=True, max_length=16)),
                ('counter', models.IntegerField(default=0)),
                ('last_attempt_at', models.DateTimeField(db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='SmsCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(db_index=True, max_length=16)),
                ('ip', models.GenericIPAddressField(db_index=True)),
                ('code', models.CharField(max_length=10)),
                ('expire_at', models.DateTimeField(db_index=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='phone',
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='username',
            field=models.CharField(help_text='Пожалуйста, укажите свой пароль', max_length=15, unique=True, validators=[krom.validators.PhoneValidator]),
        ),
    ]
