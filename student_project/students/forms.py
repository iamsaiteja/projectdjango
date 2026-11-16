from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    year = forms.IntegerField(min_value=1, max_value=6)
    class Meta:
        model = Student
        fields = ['name', 'roll_no', 'branch', 'year']
