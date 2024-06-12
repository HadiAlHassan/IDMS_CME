# Generated by Django 4.1.13 on 2024-06-11 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocGeneralInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('general_info_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('source', models.TextField()),
                ('title', models.TextField()),
                ('author', models.TextField()),
                ('nlp_id', models.IntegerField(blank=True, null=True, unique=True)),
            ],
            options={
                'db_table': 'general_info',
            },
        ),
        migrations.DeleteModel(
            name='GeneralInfo',
        ),
    ]
