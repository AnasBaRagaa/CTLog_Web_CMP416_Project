# Generated by Django 3.2.2 on 2021-05-31 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ct_helper', '0005_auto_20210531_0619'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='hospital',
            constraint=models.UniqueConstraint(fields=('hospital_website', 'owner'), name='unique_hospital_website'),
        ),
        migrations.AddConstraint(
            model_name='hospital',
            constraint=models.UniqueConstraint(fields=('hospital_phone_number', 'owner'), name='unique_hospital_phone_number'),
        ),
        migrations.AddConstraint(
            model_name='surgeon',
            constraint=models.UniqueConstraint(fields=('surgeon_Email', 'owner'), name='unique_surgeon_Email'),
        ),
        migrations.AddConstraint(
            model_name='surgeon',
            constraint=models.UniqueConstraint(fields=('surgeon_phone_number', 'owner'), name='unique_surgeon_phone_number'),
        ),
    ]