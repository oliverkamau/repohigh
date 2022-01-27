import datetime
import json
from urllib.parse import urlsplit

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_control

from feemanager.feesetup.feecategories.models import FeeCategories
from localities.models import Select2Data
from localities.serializers import Select2Serializer
from setups.academics.classes.models import SchoolClasses
from setups.system.categoryaudit.models import CategoryAudit
from studentmanager.student.models import Students
from useradmin.users.models import User

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def groupingpage(request):
    return render(request, 'fees/feegroupings.html')

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

def searchfeecategory(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    categories = FeeCategories.objects.raw(
        "SELECT top 5 category_code,category_name FROM feecategories_feecategories WHERE category_name like %s or category_desc like %s",
        tuple([query, query]))

    for obj in categories:
        text = obj.category_name
        select2 = Select2Data()
        select2.id = str(obj.category_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})

def getclassstudents(request,id):
    listsel = []
    students = Students.objects.raw(
        "SELECT student_code,student_name,adm_no FROM student_students" +
        " where student_school_status='Active' and  student_class_id = %s",
        [id]

    )

    for obj in students:
        if obj.student_code not in listsel:
            response_data = {}

            response_data['studentCode'] = obj.student_code
            response_data['name'] = obj.adm_no+'-'+obj.student_name

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)


def searchnewfeecategory(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    categories = FeeCategories.objects.raw(
        "SELECT top 5 category_code,category_name FROM feecategories_feecategories WHERE category_name like %s or category_desc like %s",
        tuple([query, query]))

    for obj in categories:
        text = obj.category_name
        select2 = Select2Data()
        select2.id = str(obj.category_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def getfeestudents(request,id,classcode):
    listsel = []
    students = Students.objects.raw(
        "SELECT student_code,student_name,adm_no FROM student_students" +
        " where student_school_status='Active' and student_class_id = %s and student_fee_category_id = %s",
        [classcode,id]

    )

    for obj in students:
        if obj.student_code not in listsel:
            response_data = {}

            response_data['studentCode'] = obj.student_code
            response_data['name'] = obj.adm_no + '-' + obj.student_name

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)


def getfeestudent(request,id):
    listsel = []
    students = Students.objects.raw(
        "SELECT student_code,student_name,adm_no FROM student_students" +
        " where student_school_status='Active' and student_fee_category_id = %s",
        [id]

    )

    for obj in students:
        if obj.student_code not in listsel:
            response_data = {}

            response_data['studentCode'] = obj.student_code
            response_data['name'] = obj.adm_no + '-' + obj.student_name

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)



def dynamicaddress(request):
    response_data = {}
    response_data['url'] = urlsplit(
        request.build_absolute_uri(None)).scheme + '://' + request.get_host() + '/static/img/spinner.gif'
    return JsonResponse(response_data)

def assignstudentcategory(request):

  if request.user.is_authenticated:
    students = request.POST.get('students', None)
    category = request.POST.get('category', None)
    newcategory = request.POST.get('newcategory', None)
    newcategories = FeeCategories.objects.get(pk=newcategory)
    # classcode = request.POST.get('classcode', None)
    unstringified =json.loads(students)

    for std in unstringified:
        print(std)
        student = Students.objects.get(pk=std)
        student.student_fee_category=newcategories
        student.save()

    categories = FeeCategories.objects.get(pk=category)
    u = User.objects.get(username=request.user)
    audit=CategoryAudit()
    audit.categoryaudit_username=u.username
    audit.categoryaudit_categoryfrom=categories.category_name
    audit.categoryaudit_categoryto=newcategories.category_name
    audit.categoryaudit_dateassigned=datetime.datetime.now()
    audit.save()

    return JsonResponse({'success':'Category Assigned Successfully'})
  else:
    return JsonResponse({'timeout': 'Your User Session expired!'})


def unassignstudentcategory(request):
    students = request.POST.get('students', None)
    category = request.POST.get('category', None)
    # newcategory = request.POST.get('newcategory', None)
    unstringified =json.loads(students)

    for std in unstringified:
        print(std)
        student = Students.objects.get(pk=std)
        categories = FeeCategories.objects.get(pk=category)
        student.student_fee_category = categories
        student.save()

    return JsonResponse({'success': 'Category Unassigned Successfully'})


def assignallcategories(request):
  if request.user.is_authenticated:
    category = request.POST.get('category', None)
    newcategory = request.POST.get('newcategory', None)
    newcategories = FeeCategories.objects.get(category_code=newcategory)
    classcode = request.POST.get('classcode', None)
    students = Students()
    if classcode is not None and category is not None:
        students = Students.objects.raw(
            "select student_code from student_students where student_class_id =%s and student_fee_category_id=%s",
            [classcode,category])

    elif classcode is None and category is not None:
        students = Students.objects.raw(
            "select student_code from student_students where student_fee_category_id=%s",
            [category])
    elif classcode is not None and category is  None:
        students = Students.objects.raw(
            "select student_code from student_students where student_class_id=%s",
            [classcode])


    for obj in students:

        std = obj.student_code
        student = Students.objects.get(pk=std)
        student.student_fee_category=newcategories
        student.save()

    categories = FeeCategories.objects.get(pk=category)
    u = User.objects.get(username=request.user)
    audit = CategoryAudit()
    audit.categoryaudit_username = u.username
    audit.categoryaudit_categoryfrom = categories.category_name
    audit.categoryaudit_categoryto = newcategories.category_name
    audit.categoryaudit_dateassigned = datetime.datetime.now()
    audit.save()

    return JsonResponse({'success': 'Categories Assigned Successfully'})
  else:
    return JsonResponse({'timeout': 'Your User Session expired!'})


def unassignallcategories(request):
    category = request.POST.get('category', None)
    newcategory = request.POST.get('newcategory', None)
    classcode = request.POST.get('classcode', None)
    students = Students()
    if newcategory is not None and category is not None:
        students = Students.objects.raw(
            "select student_code from student_students where student_class_id =%s and student_fee_category_id=%s",
            [classcode, newcategory])

    elif classcode is None and newcategory is not None:
        students = Students.objects.raw(
            "select student_code from student_students where student_fee_category_id=%s",
            [newcategory])
    elif classcode is not None and newcategory is None:
        students = Students.objects.raw(
            "select student_code from student_students where student_class_id=%s",
            [classcode])

    for obj in students:
        std = obj.student_code
        student = Students.objects.get(pk=std)
        categories = FeeCategories.objects.get(category_code=category)
        student.student_fee_category = categories
        student.save()

    return JsonResponse({'success': 'Categories Unassigned Successfully'})


def getnewfeestudents(request,id,classcode):
    listsel = []
    students = Students.objects.raw(
        "SELECT student_code,student_name,adm_no FROM student_students" +
        " where student_school_status='Active' and student_class_id = %s and student_fee_category_id = %s",
        [classcode, id]

    )

    for obj in students:
        if obj.student_code not in listsel:
            response_data = {}

            response_data['studentCode'] = obj.student_code
            response_data['name'] = obj.adm_no + '-' + obj.student_name

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)


def getnewfeestudent(request,id):
    listsel = []
    students = Students.objects.raw(
        "SELECT student_code,student_name,adm_no FROM student_students" +
        " where student_school_status='Active' and student_fee_category_id = %s",
        [id]

    )

    for obj in students:
        if obj.student_code not in listsel:
            response_data = {}

            response_data['studentCode'] = obj.student_code
            response_data['name'] = obj.adm_no + '-' + obj.student_name

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)