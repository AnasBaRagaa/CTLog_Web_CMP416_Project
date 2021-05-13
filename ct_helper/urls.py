from django.urls import path
from . import views

app_name = 'ct_helper'
urlpatterns = [
    path('', views.index, name='index'),
    #
    # # hospitals urls
    path('hospitals/', views.HospitalListView.as_view(), name='hospitals'),
    path('hospitals/add/', views.HospitalCreateView.as_view(extra_context={'title': 'Add Hospital'}),
         name='hospitals_add'),
    path('hospitals/update/<int:pk>/', views.HospitalUpdateView.as_view(extra_context={'title': 'Update Hospital'}),
         name='hospitals_update'),
    path('hospitals/delete/<int:pk>/', views.HospitalDeleteView.as_view(extra_context={'title': 'Delete Hospital'}),
         name='hospitals_delete'),
    #
    # # patients urls
    path('patients/', views.PatientListView.as_view(), name='patients'),
    path('patients/add/', views.PatientCreateView.as_view(extra_context={'title': 'Add Patient'}), name='patients_add'),
    path('patients/update/<int:pk>/', views.PatientUpdateView.as_view(extra_context={'title': 'Update Patient'}),
         name='patients_update'),
    path('patients/delete/<int:pk>/', views.PatientDeleteView.as_view(extra_context={'title': 'Delete Patient'}),
         name='patients_delete'),

    # # surgeons urls
    path('surgeons/', views.SurgeonListView.as_view(), name='surgeons'),
    path('surgeons/add/', views.SurgeonCreateView.as_view(extra_context={'title': 'Add Surgeon'}), name='surgeons_add'),
    path('surgeons/update/<int:pk>/', views.SurgeonUpdateView.as_view(extra_context={'title': 'Update Surgeon'}),
         name='surgeons_update'),
    path('surgeons/delete/<int:pk>/', views.SurgeonDeleteView.as_view(extra_context={'title': 'Delete Surgeon'}),
         name='surgeons_delete'),
    #
    # # operations urls
    path('operations/', views.OperationListView.as_view(), name='operations'),
    path('operations/add/', views.OperationCreateView.as_view(extra_context={'title': 'Add Operation'}),
         name='operations_add'),
    path('operations/update/<int:pk>/',
         views.OperationUpdateView.as_view(extra_context={'title': 'Update Operation', 'update': True, }),
         name='operations_update'),
    path('operations/delete/<int:pk>/', views.OperationDeleteView.as_view(extra_context={'title': 'Delete Operation'}),
         name='operations_delete'),
    path('operations/details/<int:pk>/', views.OperationDetailView.as_view(extra_context={'title': ' Operation'}),
         name='operations_details'),
    #
    # # drugs urls
    path('drugs/', views.DrugListView.as_view(), name='drugs'),
    path('drugs/add/', views.DrugCreateView.as_view(extra_context={'title': 'Add Drug'}), name='drugs_add'),
    path('drugs/update/<int:pk>/', views.DrugUpdateView.as_view(extra_context={'title': 'Update Drug'}),
         name='drugs_update'),
    path('drugs/delete/<int:pk>/', views.DrugDeleteView.as_view(extra_context={'title': 'Delete Drug'}),
         name='drugs_delete'),

    # Prescriptions urls
    path('prescriptions/add/<int:operation>/',
         views.PrescriptionCreateView.as_view(extra_context={'title': 'Add Prescription'}),
         name='prescriptions_add'),
    path('prescriptions/update/<int:pk>/', views.PrescriptionUpdateView.as_view(
        extra_context={'title': 'Update Prescription'}),name='prescriptions_update'),
    path('prescriptions/delete/<int:pk>/', views.PrescriptionDeleteView.as_view(
        extra_context={'title': 'Delete Prescription'}), name='prescriptions_delete'),

    # Tests urls
    path('tests/add/<int:operation>/<str:order>/', views.TestCreateView.as_view( extra_context={'title': 'Add Tests'}), name='tests_add'),
    path('tests/update/<int:pk>/', views.TestUpdateView.as_view(extra_context={'title': 'Update Tests'}), name='tests_update'),
    path('tests/delete/<int:pk>/', views.TestDeleteView.as_view(extra_context={'title': 'Delete Tests'}), name='tests_delete'),

]

