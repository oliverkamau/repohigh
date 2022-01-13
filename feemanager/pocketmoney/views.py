from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from localities.models import Select2Data
from localities.serializers import Select2Serializer
from setups.academics.classes.models import SchoolClasses
from studentmanager.student.models import Students


def pocketmoneypage(request):
    return render(request, 'fees/pocketmoney.html')


def searchclass(request):
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

def searchstudents(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    students = Students.objects.raw(
        "SELECT top 5 student_code,adm_no,student_name from student_students where " +
        " adm_no like %s or student_name like %s",
        [query, query])

    for obj in students:
        text = obj.student_name + '-' + obj.adm_no
        select2 = Select2Data()
        select2.id = str(obj.student_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


