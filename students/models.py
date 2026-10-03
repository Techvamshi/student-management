from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    duration = models.CharField(max_length=50, help_text="e.g. 3 years")
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Student(models.Model):
    GENDER_CHOICES = [("Male", "Male"), ("Female", "Female"), ("Other", "Other")]

    student_id = models.CharField("Student ID", max_length=20, unique=True)
    name = models.CharField("Student name", max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField("Phone number", max_length=20)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name="students")
    department = models.CharField(max_length=100)
    joining_date = models.DateField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.student_id} - {self.name}"
