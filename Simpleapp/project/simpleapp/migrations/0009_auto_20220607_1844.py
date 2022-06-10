# Generated by Django 3.2.13 on 2022-06-07 15:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('simpleapp', '0008_auto_20220603_1207'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catsubs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
                ('catsubs_to_cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simpleapp.category')),
                ('catsubs_to_subs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='cat_subscribers',
            field=models.ManyToManyField(through='simpleapp.Catsubs', to=settings.AUTH_USER_MODEL),
        ),
    ]
