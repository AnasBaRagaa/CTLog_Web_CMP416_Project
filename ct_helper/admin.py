from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Patient)
admin.site.register(Surgeon)
admin.site.register(Hospital)
admin.site.register(Operation)
admin.site.register(Test)
admin.site.register(Prescription)
admin.site.register(Drug)

