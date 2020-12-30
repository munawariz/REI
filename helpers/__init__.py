from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from django import forms

from django.forms.models import model_to_dict 
  
def calculate_age(birthDate):
    days_in_year = 365    
    age = int((date.today() - birthDate).days / days_in_year) 
    return age 

def active_semester():    
    try:
        from sekolah.models import Semester
        return Semester.objects.get(is_active=True)        
    except ObjectDoesNotExist:
        return None

def get_initial(object):
    object_dict = model_to_dict(object)
    initial = {}
    for key, value in object_dict.items():
        initial[key] = value
    
    return initial

def form_value(valid_form: forms):
    field_value = {}
    for key, value in valid_form.cleaned_data.items():
        field_value[key] = value

    return field_value