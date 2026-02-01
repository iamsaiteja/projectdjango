from django.shortcuts import render, redirect
from .models import Student


def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {
        'students': students
    })


def add_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        roll_no = request.POST.get('roll_no')
        branch = request.POST.get('branch')
        year = request.POST.get('year')

        Student.objects.create(
            name=name,
            roll_no=roll_no,
            branch=branch,
            year=year
        )
        return redirect('student_list')

    return render(request, 'students/add_student.html')


def edit_student(request, id):
    student = Student.objects.get(id=id)

    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.roll_no = request.POST.get('roll_no')
        student.branch = request.POST.get('branch')
        student.year = request.POST.get('year')
        student.save()
        return redirect('student_list')

    return render(request, 'students/edit_student.html', {'student': student})
def delete_student(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    return redirect('student_list')
