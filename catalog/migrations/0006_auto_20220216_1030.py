# Generated by Django 3.2.5 on 2022-02-16 05:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0005_auto_20220215_1811'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Person',
            new_name='Borrower',
        ),
        migrations.CreateModel(
            name='Librarian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identy', models.CharField(max_length=200)),
                ('contact_no', models.CharField(max_length=100)),
                ('facebook', models.CharField(max_length=200)),
                ('whatsapp', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('django_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bookinstance',
            name='librarian',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.librarian'),
        ),
    ]
