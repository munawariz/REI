from django.core.exceptions import ObjectDoesNotExist
from datetime import date 
  
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