import ast
import json
from urllib.parse import urlsplit

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_control
from rest_framework import status

from localities.models import Select2Data
from localities.serializers import Select2Serializer
from setups.academics.classes.models import SchoolClasses
from setups.academics.subjects.models import Subjects
from studentmanager.student.models import Students
from studentmanager.studentsubjects.models import StudentSubjects

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def getstudentsubject(request):
    return render(request,'students/studentsubjects.html')


def searchclasses(request):
        if request.method == 'GET' and 'query' in request.GET:
            query = request.GET['query']
            query = '%' + query + '%'
        else:
            query = '%' + '' + '%'

        listsel = []
        classes = SchoolClasses.objects.raw(
            "SELECT top 5 class_code,class_name FROM classes_schoolclasses WHERE class_name like %s or class_code like %s",
            tuple([query, query]))

        for obj in classes:
            text = obj.class_name
            select2 = Select2Data()
            select2.id = str(obj.class_code)
            select2.text = text
            serializer = Select2Serializer(select2)

            listsel.append(serializer.data)

        return JsonResponse({'results': listsel})


def searchsubjects(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    subjects = Subjects.objects.raw(
        "SELECT top 5 subject_code,subject_name FROM subjects_subjects WHERE subject_name like %s",
        tuple([query]))

    for obj in subjects:
        text = obj.subject_name
        select2 = Select2Data()
        select2.id = str(obj.subject_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def getunassignedstudents(request,classcode,subject):
    listsel = []
    students = Students.objects.raw(
        "SELECT student_code,student_name FROM student_students" +
        " where student_school_status='Active' and  student_class_id = %s and "+
        " student_code not in(select stud_subject_student_id from studentsubjects_studentsubjects"+
        " where stud_subject_class_id = %s and stud_subject_subject_id = %s)",
        [classcode,classcode,subject]

    )

    for obj in students:
        if obj.student_code not in listsel:
            response_data = {}

            response_data['studentCode'] = obj.student_code
            response_data['name'] = obj.student_name

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)


def getassignedstudents(request,classcode,subject):
    listsel = []
    students = StudentSubjects.objects.raw(
        "SELECT stud_subject_code,student_name FROM studentsubjects_studentsubjects"+
        " inner join student_students on stud_subject_student_id = student_code"+
        " where stud_subject_class_id = %s and stud_subject_subject_id = %s",
        [classcode, subject]

    )

    for obj in students:
        if obj.stud_subject_code not in listsel:
            response_data = {}

            response_data['studentCode'] = obj.stud_subject_code
            response_data['name'] = obj.student_name

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)


def assignsubjects(request):
    # students = []
    students = request.POST.get('students', None)
    subject = request.POST.get('subject', None)
    classcode = request.POST.get('classcode', None)
    unstringified =json.loads(students)

    for std in unstringified:
        print(std)
        student = Students.objects.get(pk=std)
        subjects = Subjects.objects.get(pk=subject)
        classcodes = SchoolClasses.objects.get(pk=classcode)
        studSubjects = StudentSubjects()
        studSubjects.stud_subject_student=student
        studSubjects.stud_subject_class=classcodes
        studSubjects.stud_subject_subject=subjects
        studSubjects.save()

    return JsonResponse({'success':'Assigned Successfully'})

def unassignsubjects(request):
    students = request.POST.get('students', None)
    unstringified = json.loads(students)

    for std in unstringified:
        print(std)
        studSubjects = StudentSubjects.objects.get(pk=std)
        studSubjects.delete()

    return JsonResponse({'success': 'Unassigned Successfully'})


def assignallsubjects(request):
    classcode = request.POST.get('classcode', None)
    subject = request.POST.get('subject', None)
    students = Students.objects.raw("select student_code from student_students where student_class_id =%s and student_school_status='Active'", [classcode])
    for obj in students:

        std = obj.student_code
        student = Students.objects.get(pk=std)
        subjects = Subjects.objects.get(pk=subject)
        classcodes = SchoolClasses.objects.get(pk=classcode)

        studSubjects = StudentSubjects()
        studSubjects.stud_subject_student = student
        studSubjects.stud_subject_class = classcodes
        studSubjects.stud_subject_subject = subjects
        try:
            subjectstuds = StudentSubjects.objects.get(stud_subject_student=student, stud_subject_subject=subjects,stud_subject_class=classcodes)
        except StudentSubjects.DoesNotExist:
               studSubjects.save()

    return JsonResponse({'success': 'Unassigned Successfully'})


def unassignallsubjects(request):
    classcode = request.POST.get('classcode', None)
    subject = request.POST.get('subject', None)
    students= StudentSubjects.objects.raw("select stud_subject_code from studentsubjects_studentsubjects where stud_subject_class_id =%s and stud_subject_subject_id=%s",[classcode,subject])
    for obj in students:
        std=obj.stud_subject_code
        try:
            subject = StudentSubjects.objects.get(pk=std)
            subject.delete()
        except StudentSubjects.DoesNotExist:
            return JsonResponse({'error': 'Subject doesnt exist'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse({'success': 'Unassigned Successfully'})


def dynamicaddress(request):
    response_data = {}
    response_data['url'] = urlsplit(
        request.build_absolute_uri(None)).scheme + '://' + request.get_host() + '/static/img/spinner.gif'
    return JsonResponse(response_data)

def populatemandatorysubjects(request):
    classes=SchoolClasses.objects.all()

    for cl in classes:
        subjects = Subjects.objects.all()
        for sub in subjects:
                 if sub.mandatory_subject:
                    students = Students.objects.raw("select student_code from student_students where student_class_id =%s and student_school_status='Active'",
                                        [cl.class_code])
                    for obj in students:
                       std = obj.student_code
                       student = Students.objects.get(pk=std)
                       subject = Subjects.objects.get(pk=sub.subject_code)
                       classcodes = SchoolClasses.objects.get(pk=cl.class_code)
                       studSubjects = StudentSubjects()
                       studSubjects.stud_subject_student = student
                       studSubjects.stud_subject_class = classcodes
                       studSubjects.stud_subject_subject = subject
                       try:
                         subjectstuds = StudentSubjects.objects.get(stud_subject_student=student,
                                                                    stud_subject_subject=subject,
                                                                    stud_subject_class=classcodes)
                       except StudentSubjects.DoesNotExist:
                         studSubjects.save()

    return JsonResponse({'success': 'Mandatory Subjects Assigned Successfully'})

