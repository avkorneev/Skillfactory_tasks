# Generated by Django 3.2.13 on 2022-05-17 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simpleapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('rating', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('com_text', models.CharField(max_length=255)),
                ('com_datetime', models.DateTimeField(auto_now_add=True)),
                ('com_rating', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_name', models.CharField(max_length=255)),
                ('post_text', models.TextField()),
                ('post_datetime', models.DateTimeField(auto_now_add=True)),
                ('post_type', models.CharField(choices=[('ART', 'Статья'), ('POST', 'Новость')], default='ART', max_length=255)),
                ('post_rating', models.IntegerField(default=0)),
                ('post_to_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simpleapp.author')),
            ],
        ),
        migrations.CreateModel(
            name='Postcat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='category',
            name='name',
        ),
        migrations.AddField(
            model_name='category',
            name='cat_name',
            field=models.CharField(default=1, max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.AddField(
            model_name='postcat',
            name='postcat_to_cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simpleapp.category'),
        ),
        migrations.AddField(
            model_name='postcat',
            name='postcat_to_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simpleapp.post'),
        ),
        migrations.AddField(
            model_name='post',
            name='post_to_postcat',
            field=models.ManyToManyField(through='simpleapp.Postcat', to='simpleapp.Category'),
        ),
        migrations.AddField(
            model_name='comment',
            name='com_to_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simpleapp.post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='com_to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simpleapp.user'),
        ),
        migrations.AddField(
            model_name='author',
            name='author_to_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='simpleapp.user'),
        ),
    ]