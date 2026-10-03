from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CourseForm, StudentForm
from .models import Course, Student


def dashboard(request):
    return render(request, "dashboard.html", {
        "total_students": Student.objects.count(),
        "total_courses": Course.objects.count(),
        "recent_students": Student.objects.select_related("course").order_by("-id")[:5],
        "courses": Course.objects.annotate(student_count=Count("students")),
    })


# ---------- Students ----------
def student_list(request):
    q = request.GET.get("q", "").strip()
    students = Student.objects.select_related("course")
    if q:
        students = students.filter(
            Q(name__icontains=q) | Q(student_id__icontains=q) | Q(email__icontains=q)
            | Q(phone__icontains=q) | Q(department__icontains=q) | Q(course__name__icontains=q)
        )
    return render(request, "student_list.html", {"students": students, "q": q})


def student_detail(request, pk):
    return render(request, "student_detail.html", {"student": get_object_or_404(Student, pk=pk)})


def student_add(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        student = form.save()
        return redirect("student_detail", pk=student.pk)
    return render(request, "form.html", {"form": form, "title": "Add student", "cancel": "student_list"})


def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect("student_detail", pk=student.pk)
    return render(request, "form.html", {"form": form, "title": "Edit student", "cancel": "student_list"})


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect("student_list")
    return render(request, "confirm_delete.html", {
        "title": "Delete student",
        "message": f"Delete {student.name} ({student.student_id})? This cannot be undone.",
        "cancel_url": student.get_absolute_url() if hasattr(student, "get_absolute_url") else "/students/%d/" % student.pk,
    })


# ---------- Courses ----------
def course_list(request):
    courses = Course.objects.annotate(student_count=Count("students"))
    return render(request, "course_list.html", {"courses": courses})


def course_add(request):
    form = CourseForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("course_list")
    return render(request, "form.html", {"form": form, "title": "Add course", "cancel": "course_list"})


def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    form = CourseForm(request.POST or None, instance=course)
    if form.is_valid():
        form.save()
        return redirect("course_list")
    return render(request, "form.html", {"form": form, "title": "Edit course", "cancel": "course_list"})


def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        course.delete()
        return redirect("course_list")
    count = course.students.count()
    return render(request, "confirm_delete.html", {
        "title": "Delete course",
        "message": f"Delete {course.name}? {count} student(s) will be left without a course.",
        "cancel_url": "/courses/",
    })
