from django import forms
from .models import Course, Student


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "duration", "description"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["student_id", "name", "email", "phone", "date_of_birth",
                  "gender", "course", "department", "joining_date"]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "joining_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }
