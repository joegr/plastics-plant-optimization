from django import forms
from django.forms import ModelForm, CharField
from .models import OptimizationJob, Job
from django.db import models
from django.forms import Textarea, TextInput, Select, URLInput

#Use docs for all widgets 
#https://docs.djangoproject.com/en/2.0/_modules/django/forms/widgets/
class OptimizationJobForm(ModelForm):
    title = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Sensible Name for your job',
    )
    class Meta:
        model = OptimizationJob 
        fields = ["title",]
        widgets = {
            "title": TextInput(),
        }

    #title = forms.CharField(label='Name of the Job', max_length=100)

class JobForm(ModelForm):
    class Meta:
        model = Job
        #fields = "__all__"
        fields = ["arrival_date","machines","duration",]
        #exclude=["optimization_job",]
