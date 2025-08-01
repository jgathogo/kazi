# Generated by Django 4.2.23 on 2025-07-10 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_certification_certification_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultant',
            name='firms',
            field=models.ManyToManyField(blank=True, help_text='Firms this consultant is associated with.', related_name='consultants', to='profiles.firm'),
        ),
        migrations.AlterField(
            model_name='project',
            name='firm_portfolio',
            field=models.ForeignKey(blank=True, help_text='The firm that holds this project in its portfolio. Can be empty for independent projects.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', to='profiles.firm'),
        ),
    ]
