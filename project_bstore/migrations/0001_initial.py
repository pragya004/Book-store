# Generated by Django 2.1.5 on 2019-01-30 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='book_table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.IntegerField()),
                ('books_count', models.IntegerField()),
                ('publication_year', models.IntegerField()),
                ('authors', models.TextField()),
                ('title', models.TextField()),
                ('average_rating', models.FloatField()),
                ('image_url', models.URLField()),
            ],
        ),
    ]
