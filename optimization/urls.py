"""optimization URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from plastics import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("solve/<int:pk>/",views.solve, name='solve'),
    path("",views.home, name='home'),
    path("create_job/", views.create_new_optimization_job, name="create_new_optimization_job"),
    path("job/<int:pk>/",views.optimization_job, name='optimization_job_details'),
    path("job/<int:pk>/create/",views.optimization_job, name='create_optimization_job'),
    path("job/<int:pk>/clear_all_solution_sets/",views.clear_all_solution_sets, name='clear_all_solution_sets'),

]
