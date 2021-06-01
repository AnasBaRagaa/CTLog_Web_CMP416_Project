# Anas Ba Ragaa _ b00075797

"""
Superuser :
    username: user
    pass: x

Test users:
username= testuser1
pass = xxxx

username= testuser2
pass = xxxx

username= testuser3
pass = xxxx
"""
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from datetime import date

phone_regex = RegexValidator(regex=r'^(00|[+]){0,1}(971){0,1}[1-9]{1}[0-9]{7,8}$',
                             message="Phone number must be entered in this format : 503456789, +971503456789 or "
                                     "62345678   ")

GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

TIME_CHOICES = (('PRE', 'Pre operation'), ('POST', 'Post operation'))

TEST_CHOICES = (('P', 'Positive'), ('N', 'Negative'))
number_validator = RegexValidator(regex=r'^[0-9]{1,20}', message='Insert less than 20 digits')


class Surgeon(models.Model):
    surgeon_name = models.CharField(max_length=80)
    surgeon_address = models.CharField(max_length=200)
    surgeon_Email = models.EmailField(max_length=50)

    surgeon_phone_number = models.CharField(validators=[phone_regex], max_length=14, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['surgeon_name','owner'], name='unique_surgeon_name'),
            # models.UniqueConstraint(fields=['surgeon_Email', 'owner'], name='unique_surgeon_Email'),
            # models.UniqueConstraint(fields=['surgeon_phone_number', 'owner'], name='unique_surgeon_phone_number'),
        ]

    def __str__(self):
        return self.surgeon_name


class Hospital(models.Model):
    hospital_name = models.CharField(max_length=100)
    hospital_address = models.CharField(max_length=200)
    hospital_website = models.URLField(max_length=200, blank=True, null=True)

    hospital_phone_number = models.CharField(validators=[phone_regex], max_length=14, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['hospital_name','owner'], name='unique_hospital_name'),
           # models.UniqueConstraint(fields=['hospital_website', 'owner'], name='unique_hospital_website'),
           # models.UniqueConstraint(fields=['hospital_phone_number', 'owner'], name='unique_hospital_phone_number'),
        ]

    def __str__(self):
        return self.hospital_name


class Patient(models.Model):
    patient_name = models.CharField(max_length=80)

    patient_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    patient_address = models.CharField(max_length=200)
    patient_Email = models.EmailField(max_length=50)
    patient_Nationality = CountryField()

    patient_phone_number = models.CharField(validators=[phone_regex], max_length=14, blank=True, null=True)
    patient_date_of_birth = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    file_number = models.CharField(max_length=20, validators=[number_validator])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['patient_name', 'hospital','owner'], name='unique_patient_hospital'),
            models.UniqueConstraint(fields=['file_number', 'hospital','owner'], name='unique_file-number_hospital'),

        ]

    def __str__(self):
        return self.patient_name + ' ,  ' + self.hospital.hospital_name

    def get_age_now(self):  # to view the patient age as part of the patient profile
        today = date.today()
        born = self.patient_date_of_birth
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class Operation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    pre_operation_clinical = models.CharField(max_length=500)
    admission_date = models.DateTimeField()
    surgeon = models.ForeignKey(Surgeon, on_delete=models.CASCADE)
    anesthesia = models.CharField(max_length=200, blank=True, null=True)
    perfusionist = models.CharField(max_length=200, blank=True, null=True)
    diagnosis = models.CharField(max_length=200)
    operation_name = models.CharField(max_length=200)
    operation_details = models.CharField(max_length=500, blank=True, null=True)
    operation_date = models.DateTimeField()
    post_operation_clinical = models.CharField(max_length=500, blank=True, null=True)
    discharge_date = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, blank=True,
                                 null=True)  # copy hospital in case patient.hospital changes after the operation

    def __str__(self):
        return self.operation_name + ',  patient : ' + self.patient.patient_name + ', in :  ' + self.hospital.hospital_name

    def get_age(self):  # to view the patient age at the time of the operation
        op = self.operation_date
        born = self.patient.patient_date_of_birth
        return op.year - born.year - ((op.month, op.day) < (born.month, born.day))

    def get_pre_tests(self):
        return self.test_set.filter(order='PRE')

    def get_post_tests(self):
        return self.test_set.filter(order='POST')


class Test(models.Model):
    order = models.CharField(max_length=4, choices=TIME_CHOICES)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    hIV = models.CharField(max_length=1, choices=TEST_CHOICES, null=True, blank=True)
    hBV = models.CharField(max_length=1, choices=TEST_CHOICES, null=True, blank=True)
    hCV = models.CharField(max_length=1, choices=TEST_CHOICES, null=True, blank=True)
    cRP = models.CharField(max_length=1, choices=TEST_CHOICES, null=True, blank=True)
    hP = models.DecimalField(decimal_places=2, blank=True, null=True, max_digits=4, help_text='0.0 - 20.0',
                             validators=[MaxValueValidator(20.0), MinValueValidator(0.0)], )
    hBA1C = models.DecimalField(decimal_places=2, blank=True, null=True, max_digits=4,help_text='0.0 - 20.0',
                                validators=[MaxValueValidator(20.0), MinValueValidator(0.0)])
    creatine = models.DecimalField(decimal_places=2, blank=True, null=True, max_digits=4,help_text='0.0 - 30.0',
                                   validators=[MaxValueValidator(30.0), MinValueValidator(0.0)])
    urea = models.DecimalField(decimal_places=1, blank=True, null=True, max_digits=4,help_text='0.0 - 200.0',
                               validators=[MaxValueValidator(200.0), MinValueValidator(0.0)])
    gFR = models.DecimalField(decimal_places=1, blank=True, null=True, max_digits=4,help_text='0.0 - 200.0',
                              validators=[MaxValueValidator(200.0), MinValueValidator(0.0)])
    nA = models.DecimalField(decimal_places=1, blank=True, null=True, max_digits=4,help_text='0.0 - 200.0',
                             validators=[MaxValueValidator(200.0), MinValueValidator(0.0)])
    k = models.DecimalField(decimal_places=1, blank=True, null=True, max_digits=4,help_text='0.0 - 200.0',
                            validators=[MaxValueValidator(200.0), MinValueValidator(0.0)])
    aLT = models.DecimalField(decimal_places=1, blank=True, null=True, max_digits=4,help_text='0.0 - 300.0',
                              validators=[MaxValueValidator(300.0), MinValueValidator(0.0)])
    aST = models.DecimalField(decimal_places=1, blank=True, null=True, max_digits=4,help_text='0.0 - 300.0',
                              validators=[MaxValueValidator(300.0), MinValueValidator(0.0)])
    platelt = models.DecimalField(decimal_places=1, blank=True, null=True, max_digits=4,help_text='0.0 - 500.0',
                                  validators=[MaxValueValidator(500.0), MinValueValidator(0.0)])
    wBC = models.DecimalField(decimal_places=1, blank=True, null=True, max_digits=4,help_text='0.0 - 700.0',
                              validators=[MaxValueValidator(700.0), MinValueValidator(0.0)])
    lDL = models.DecimalField(decimal_places=1, blank=True, null=True, max_digits=5,help_text='0.0 - 1000.0',
                              validators=[MaxValueValidator(1000.0), MinValueValidator(0.0)])
    hDL = models.DecimalField(decimal_places=1, blank=True, null=True, max_digits=5,help_text='0.0 - 1000.0',
                              validators=[MaxValueValidator(1000.0), MinValueValidator(0.0)])
    tSH = models.DecimalField(decimal_places=1, blank=True, null=True, max_digits=5,help_text='0.0 - 1000.0',
                              validators=[MaxValueValidator(1000.0), MinValueValidator(0.0)])
    t3 = models.DecimalField(decimal_places=1, blank=True, null=True, max_digits=5,help_text='0.0 - 1000.0',
                             validators=[MaxValueValidator(1000.0), MinValueValidator(0.0)])
    t4 = models.DecimalField(decimal_places=1, blank=True, null=True, max_digits=5,help_text='0.0 - 1000.0',
                             validators=[MaxValueValidator(1000.0), MinValueValidator(0.0)])
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        # To ensure each operation can have only one pre operation Test and one post operation Test
        constraints = [
            models.UniqueConstraint(fields=['order', 'operation'], name='unique_test_operation'),
        ]

    def __iter__(self):
        for field_name in self._meta.get_fields():
            ignore = ['id', 'order', 'operation', 'owner']
            if field_name.name not in ignore:
                value = getattr(self, field_name.name, None)
                yield field_name.name.upper(), value

    def __str__(self):

        if self.order == 'PRE':
            return 'pre operation tests for ' + str(self.operation)
        return 'post operation tests for ' + str(self.operation)


class Drug(models.Model):
    drug_name = models.CharField(max_length=100)
    drug_description = models.CharField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['drug_name','owner'], name='unique_drug_name'),
        ]

    def __str__(self):
        return self.drug_name


class Prescription(models.Model):
    """
    I can't make prescription many-to-many with operation and drugs because each prescription will consist of a single
     drug reference,single operation reference, because it will also contain the dose and the duration fields because
     they vary based on the patient. Thus I believe this is a better design.
    One Operation  can be assigned to different prescriptions
    One Drug can be assigned to different prescriptions

    """

    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    dose = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.drug) + ', ' + self.dose + ' , for ' + self.duration

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['drug', 'operation'], name='unique_user_post'),
        ]
