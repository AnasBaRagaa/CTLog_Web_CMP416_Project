from django.urls import path
from . import views

app_name = 'ct_helper'
urlpatterns = [
    path('', views.index, name='index'),
    #
    # # hospitals urls
    # path('hospitals/', views.DetailView.as_view(), name='hospitals'),
    # path('hospitals/add/', views.DetailView.as_view(), name='hospitals_add'),
    # path('hospitals/update/<int:pk>/', views.DetailView.as_view(), name='hospitals_update'),
    # path('hospitals/delete/<int:pk>/', views.DetailView.as_view(), name='hospitals_delete'),
    #
    # # patients urls
    # path('patients/', views.DetailView.as_view(), name='patients'),
    # path('patients/add/', views.DetailView.as_view(), name='patients_add'),
    # path('patients/update/<int:pk>/', views.DetailView.as_view(), name='patients_update'),
    # path('patients/delete/<int:pk>/', views.DetailView.as_view(), name='patients_delete'),
    #
    # # surgeons urls
    # path('surgeons/', views.DetailView.as_view(), name='surgeons'),
    # path('surgeons/add/', views.DetailView.as_view(), name='surgeons_add'),
    # path('surgeons/update/<int:pk>/', views.DetailView.as_view(), name='surgeons_update'),
    # path('surgeons/delete/<int:pk>/', views.DetailView.as_view(), name='surgeons_delete'),
    #
    # # operations urls
    # path('operations/', views.DetailView.as_view(), name='operations'),
    # path('operations/add/<int:patient>/', views.DetailView.as_view(), name='operations_add'),
    # path('operations/update/<int:pk>/', views.DetailView.as_view(), name='operations_update'),
    # path('operations/delete/<int:pk>/', views.DetailView.as_view(), name='operations_delete'),
    # path('operations/details/<int:pk>/', views.DetailView.as_view(), name='operations_details'),
    #
    # # drugs urls
    # path('drugs/', views.DetailView.as_view(), name='drugs'),
    # path('drugs/add/', views.DetailView.as_view(), name='drugs_add'),
    # path('drugs/update/<int:pk>/', views.DetailView.as_view(), name='drugs_update'),
    # path('drugs/delete/<int:pk>/', views.DetailView.as_view(), name='drugs_delete'),
    #
    # # Prescriptions urls
    # path('prescriptions/add/<int:operation>/<str:order>/', views.DetailView.as_view(), name='prescriptions_add_order'),
    # path('prescriptions/update/<int:pk>/', views.DetailView.as_view(), name='prescriptions_update'),
    # path('prescriptions/delete/<int:pk>/', views.DetailView.as_view(), name='prescriptions_delete'),
    #
    # # Tests urls
    # path('tests/add/<int:operation>/<str:order>/', views.DetailView.as_view(), name='tests_add'),
    # path('tests/update/<int:pk>/', views.DetailView.as_view(), name='tests_update'),
    # path('tests/delete/<int:pk>/', views.DetailView.as_view(), name='tests_delete'),

]
