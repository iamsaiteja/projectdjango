from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Student
from .forms import StudentForm

@staff_member_required
def student_list(request):
    return render(request, 'students/student_list.html', {'students': Student.objects.all()})

@staff_member_required
def add_student(request):
    form = StudentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'students/add_student.html', {'form': form})

@staff_member_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    form = StudentForm(request.POST or None, instance=student)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'students/edit_student.html', {'form': form, 'student': student})

@staff_member_required
@require_POST
def delete_student(request, id):
    get_object_or_404(Student, id=id).delete()
    return redirect('student_list')
