from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class RadioInput(forms.RadioSelect):
    input_type = 'radio'

class EmailInput(forms.EmailInput):
    input_type = 'email'

class PasswordInput(forms.PasswordInput):
    input_type = 'password'