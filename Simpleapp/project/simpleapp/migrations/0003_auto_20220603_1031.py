# Generated by Django 3.2.13 on 2022-06-03 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simpleapp', '0002_auto_20220517_1342'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='author',
            name='author_to_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='simpleapp.users'),
        ),
    ]
