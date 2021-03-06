# Generated by Django 3.2.2 on 2021-05-08 14:32

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drug_name', models.CharField(max_length=100)),
                ('drug_description', models.CharField(max_length=500)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hospital_name', models.CharField(max_length=100)),
                ('hospital_address', models.CharField(max_length=200)),
                ('hospital_website', models.URLField(blank=True, null=True)),
                ('hospital_phone_number', models.CharField(blank=True, max_length=14, null=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in this format : 503456789, +971503456789 or 62345678   ', regex='^(00|[+]){0,1}(971){0,1}[1-9]{1}[0-9]{7,8}$')])),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pre_operation_clinical', models.CharField(max_length=500)),
                ('admission_date', models.DateTimeField()),
                ('anesthesia', models.CharField(blank=True, max_length=200, null=True)),
                ('perfusionist', models.CharField(blank=True, max_length=200, null=True)),
                ('diagnosis', models.CharField(max_length=200)),
                ('operation_name', models.CharField(max_length=200)),
                ('operation_details', models.CharField(blank=True, max_length=500, null=True)),
                ('operation_date', models.DateTimeField()),
                ('post_operation_clinical', models.CharField(blank=True, max_length=500, null=True)),
                ('discharge_date', models.DateTimeField(blank=True, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.CharField(choices=[('PRE', 'Pre operation'), ('POST', 'Post operation')], max_length=4)),
                ('hIV', models.CharField(blank=True, choices=[('P', 'Positive'), ('N', 'Negative')], max_length=1, null=True)),
                ('hBV', models.CharField(blank=True, choices=[('P', 'Positive'), ('N', 'Negative')], max_length=1, null=True)),
                ('hCV', models.CharField(blank=True, choices=[('P', 'Positive'), ('N', 'Negative')], max_length=1, null=True)),
                ('cRP', models.CharField(blank=True, choices=[('P', 'Positive'), ('N', 'Negative')], max_length=1, null=True)),
                ('hP', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, validators=[django.core.validators.MaxValueValidator(20.0), django.core.validators.MinValueValidator(0.0)])),
                ('hBA1C', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, validators=[django.core.validators.MaxValueValidator(20.0), django.core.validators.MinValueValidator(0.0)])),
                ('creatine', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, validators=[django.core.validators.MaxValueValidator(30.0), django.core.validators.MinValueValidator(0.0)])),
                ('urea', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, validators=[django.core.validators.MaxValueValidator(200.0), django.core.validators.MinValueValidator(0.0)])),
                ('gFR', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, validators=[django.core.validators.MaxValueValidator(200.0), django.core.validators.MinValueValidator(0.0)])),
                ('nA', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, validators=[django.core.validators.MaxValueValidator(200.0), django.core.validators.MinValueValidator(0.0)])),
                ('k', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, validators=[django.core.validators.MaxValueValidator(200.0), django.core.validators.MinValueValidator(0.0)])),
                ('aLT', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, validators=[django.core.validators.MaxValueValidator(300.0), django.core.validators.MinValueValidator(0.0)])),
                ('aST', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, validators=[django.core.validators.MaxValueValidator(300.0), django.core.validators.MinValueValidator(0.0)])),
                ('platelt', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, validators=[django.core.validators.MaxValueValidator(500.0), django.core.validators.MinValueValidator(0.0)])),
                ('wBC', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, validators=[django.core.validators.MaxValueValidator(700.0), django.core.validators.MinValueValidator(0.0)])),
                ('lDL', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, validators=[django.core.validators.MaxValueValidator(1000.0), django.core.validators.MinValueValidator(0.0)])),
                ('hDL', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, validators=[django.core.validators.MaxValueValidator(1000.0), django.core.validators.MinValueValidator(0.0)])),
                ('tSH', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, validators=[django.core.validators.MaxValueValidator(1000.0), django.core.validators.MinValueValidator(0.0)])),
                ('t3', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, validators=[django.core.validators.MaxValueValidator(1000.0), django.core.validators.MinValueValidator(0.0)])),
                ('t4', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, validators=[django.core.validators.MaxValueValidator(1000.0), django.core.validators.MinValueValidator(0.0)])),
                ('operation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ct_helper.operation')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Surgeon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surgeon_name', models.CharField(max_length=80)),
                ('surgeon_address', models.CharField(max_length=200)),
                ('surgeon_Email', models.EmailField(max_length=50)),
                ('surgeon_phone_number', models.CharField(blank=True, max_length=14, null=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in this format : 503456789, +971503456789 or 62345678   ', regex='^(00|[+]){0,1}(971){0,1}[1-9]{1}[0-9]{7,8}$')])),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.CharField(choices=[('PRE', 'Pre operation'), ('POST', 'Post operation')], max_length=4)),
                ('dose', models.CharField(max_length=50)),
                ('duration', models.CharField(max_length=50)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ct_helper.drug')),
                ('operation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ct_helper.operation')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_name', models.CharField(max_length=80)),
                ('patient_gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('patient_address', models.CharField(max_length=200)),
                ('patient_Email', models.EmailField(max_length=50)),
                ('patient_Nationality', django_countries.fields.CountryField(max_length=2)),
                ('patient_phone_number', models.CharField(blank=True, max_length=14, null=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in this format : 503456789, +971503456789 or 62345678   ', regex='^(00|[+]){0,1}(971){0,1}[1-9]{1}[0-9]{7,8}$')])),
                ('patient_date_of_birth', models.DateTimeField()),
                ('file_number', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Insert less than 20 digits', regex='^[0-9]{1,20}')])),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ct_helper.hospital')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='operation',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ct_helper.patient'),
        ),
        migrations.AddField(
            model_name='operation',
            name='surgeon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ct_helper.surgeon'),
        ),
        migrations.AddConstraint(
            model_name='test',
            constraint=models.UniqueConstraint(fields=('order', 'operation'), name='unique_test_operation'),
        ),
        migrations.AddConstraint(
            model_name='surgeon',
            constraint=models.UniqueConstraint(fields=('surgeon_name',), name='unique_surgeon_name'),
        ),
        migrations.AddConstraint(
            model_name='prescription',
            constraint=models.UniqueConstraint(fields=('drug', 'operation'), name='unique_user_post'),
        ),
        migrations.AddConstraint(
            model_name='patient',
            constraint=models.UniqueConstraint(fields=('patient_name', 'hospital'), name='unique_patient_hospital'),
        ),
        migrations.AddConstraint(
            model_name='hospital',
            constraint=models.UniqueConstraint(fields=('hospital_name',), name='unique_hospital_name'),
        ),
        migrations.AddConstraint(
            model_name='drug',
            constraint=models.UniqueConstraint(fields=('drug_name',), name='unique_drug_name'),
        ),
    ]
