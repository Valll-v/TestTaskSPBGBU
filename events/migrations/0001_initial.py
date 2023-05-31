# Generated by Django 3.2.6 on 2023-05-31 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=400, null=True)),
                ('image', models.FileField(upload_to='images/')),
                ('date', models.DateField()),
                ('organizations', models.ManyToManyField(to='organizations.Organization')),
            ],
        ),
    ]