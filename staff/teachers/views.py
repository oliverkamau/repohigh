import json
from urllib.parse import urlsplit

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status

from localities.models import Select2Data
from localities.serializers import Select2Serializer
from setups.academics.classes.models import SchoolClasses
from setups.academics.departments.models import Departments
from setups.academics.responsibilities.models import Responsibilities
from setups.academics.subjects.models import Subjects
from staff.teachers.forms import TeacherForm
from staff.teachers.models import TeacherSalution, Teachers
from staff.teachersubjects.models import TeacherSubjects
from django.db import connection


def teacherpage(request):
    return render(request,'staff/teachers.html')


def searchtitle(request):

    vendor=connection.vendor
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    mysql='SELECT salutation_id,salutation_name FROM teachers_teachersalution WHERE salutation_name like %s or salutation_desc like %s LIMIT 5'
    mssql="SELECT top 5 salutation_id,salutation_name FROM teachers_teachersalution WHERE salutation_name like %s or salutation_desc like %s"
    usedquery = ''
    if(vendor == 'microsoft'):
        usedquery = mssql
    else:
        usedquery = mysql

    titles = TeacherSalution.objects.raw(usedquery,
        tuple([query, query]))

    for obj in titles:
        text = obj.salutation_name
        select2 = Select2Data()
        select2.id = str(obj.salutation_id)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})

def searchresponsibility(request):
    vendor=connection.vendor

    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    mysql = "SELECT rb_code,rb_name FROM responsibilities_responsibilities WHERE rb_ts='T' and rb_name like %s LIMIT 5"
    mssql = "SELECT top 5 rb_code,rb_name FROM responsibilities_responsibilities WHERE rb_ts='T' and rb_name like %s"
    usedquery = ''
    if (vendor == 'microsoft'):
        usedquery = mssql
    else:
        usedquery = mysql
    responsibility = Responsibilities.objects.raw(usedquery,
       [ query])

    for obj in responsibility:
        text = obj.rb_name
        select2 = Select2Data()
        select2.id = str(obj.rb_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})

def searchteachers(request):
    vendor=connection.vendor

    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    mysql = "SELECT teacher_code,teacher_name FROM teachers_teachers WHERE status='Active' and (teacher_name like %s or tsc_no like %s) LIMIT 5"
    mssql = "SELECT top 5 teacher_code,teacher_name FROM teachers_teachers WHERE status='Active' and (teacher_name like %s or tsc_no like %s)"
    usedquery = ''
    if (vendor == 'microsoft'):
        usedquery = mssql
    else:
        usedquery = mysql
    teachers = Teachers.objects.raw(usedquery,
       [ query,query])

    for obj in teachers:
        text = obj.teacher_name
        select2 = Select2Data()
        select2.id = str(obj.teacher_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})

def searchdepartment(request):
    vendor=connection.vendor

    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    mysql = "SELECT dp_code,dp_name FROM departments_departments WHERE dp_name like %s LIMIT 5"
    mssql = "SELECT top 5 dp_code,dp_name FROM departments_departments WHERE dp_name like %s"
    usedquery = ''
    if (vendor == 'microsoft'):
        usedquery = mssql
    else:
        usedquery = mysql
    departments = Departments.objects.raw(usedquery,
       [query])

    for obj in departments:
        text = obj.dp_name
        select2 = Select2Data()
        select2.id = str(obj.dp_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def addteachers(request):

    teacher = TeacherForm(request.POST, request.FILES)


    rs = teacher.data['responsibility']
    tt = teacher.data['title']
    dp = teacher.data['department']

    if rs is not None and rs != '':
        resp = Responsibilities.objects.get(pk=rs)
        teacher.responsibility = resp

    if tt is not None and tt != '':
        title = TeacherSalution.objects.get(pk=tt)
        teacher.title = title

    if dp is not None and dp != '':
        dept = Departments.objects.get(pk=dp)
        teacher.department = dept

    inst = teacher.save()
    tp = Teachers.objects.get(pk=inst.pk)
    tp.staff_number='T00'+str(tp.teacher_code)
    tp.save()
    return JsonResponse({'success': 'Teacher Saved Successfully'})


def getteachers(request):

 listsel = []

 teachers = Teachers.objects.raw("select teacher_code,teacher_name,gender,phone_number,email,box_address,tsc_no,date_joined,id_no,salutation_name,rb_name,dp_name  from teachers_teachers"+
" inner join responsibilities_responsibilities rr on teachers_teachers.responsibility_id = rr.rb_code"+
" inner join departments_departments dd on teachers_teachers.department_id = dd.dp_code"+
" inner join teachers_teachersalution tt on teachers_teachers.title_id = tt.salutation_id")

 for obj in teachers:
     response_data={}
     response_data['teacherCode']=obj.teacher_code
     response_data['staffNo'] = obj.staff_number
     response_data['name']=obj.salutation_name+'. '+obj.teacher_name
     response_data['phone']=obj.phone_number
     response_data['email']=obj.email
     response_data['address']=obj.box_address
     response_data['responsibility']=obj.rb_name
     response_data['admDate']=obj.date_joined.strftime("%d/%m/%Y")
     response_data['tscNo']=obj.tsc_no
     response_data['idNo']=obj.id_no
     response_data['department']=obj.dp_name
     if obj.gender == 'M':
         response_data['gender'] = "Male"
     elif obj.gender == 'F':
         response_data['gender'] = "Female"
     else:
         response_data['gender'] = "Other"

     listsel.append(response_data)

 return JsonResponse(listsel,safe=False)


def editteacher(request,id):
    response_data = {}
    teacher = Teachers.objects.get(pk=id)
    response_data['staffNo'] = teacher.staff_number

    if teacher.responsibility is not None:
       rb = Responsibilities.objects.get(pk=teacher.responsibility.pk)
       response_data['rb_code'] = rb.rb_code
       response_data['rb_name'] = rb.rb_name

    if teacher.department is not None:
       dp = Departments.objects.get(pk=teacher.department.pk)
       response_data['dp_code'] = dp.dp_code
       response_data['dp_name'] = dp.dp_name

    if teacher.title is not None:
       tt = TeacherSalution.objects.get(pk=teacher.title.pk)
       response_data['title_code'] = tt.salutation_id
       response_data['title_name'] = tt.salutation_name

    response_data['teacher_code'] = teacher.teacher_code
    response_data['teacher_name'] = teacher.teacher_name
    response_data['phone_number'] = teacher.phone_number
    response_data['email'] = teacher.email
    response_data['gender'] = teacher.gender
    response_data['status'] = teacher.status
    response_data['box_address'] = teacher.box_address

    if teacher.date_joined:
       response_data['date_joined'] = teacher.date_joined.strftime("%Y-%m-%d")
    response_data['tsc_no'] = teacher.tsc_no
    response_data['id_no'] = teacher.id_no

    if teacher.date_left:
       response_data['date_left'] = teacher.date_left.strftime("%Y-%m-%d")
    response_data['intials'] = teacher.intials
    if teacher.teacher_pic:
        response_data['url'] = urlsplit(
            request.build_absolute_uri(None)).scheme + '://' + request.get_host() + teacher.teacher_pic.url

    return JsonResponse(response_data)


def deleteteacher(request,id):
    teacher = Teachers.objects.get(pk=id)
    teacher.delete()
    return JsonResponse({'success':'Teacher Deleted Successfully'})


def updateteachers(request,id):
    teachers = Teachers.objects.get(pk=id)

    form = TeacherForm(request.POST, request.FILES, instance=teachers)

    form.save()
    return JsonResponse({'success': 'Teacher Updated Successfully'})


def getunassignedsubjects(request,id,cl):
    listsel = []
    teachers = Subjects.objects.raw(
        "SELECT subject_code,subject_name FROM subjects_subjects" +
        " where subject_code not in(select teacher_subjectsubject_id from teachersubjects_teachersubjects" +
        " where teacher_subjectteacher_id = %s and teacher_subjectclass_id = %s)",
        [id,cl]

    )

    for obj in teachers:
        if obj.subject_code not in listsel:
            response_data = {}

            response_data['subjectCode'] = obj.subject_code
            response_data['subjectName'] = obj.subject_name

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)


def getassignedsubjects(request,id,cl):
    listsel = []
    teachers = TeacherSubjects.objects.raw(
        "SELECT teacher_subjectcode,subject_name FROM teachersubjects_teachersubjects"+
        " inner join subjects_subjects on teacher_subjectsubject_id=subject_code" +
        " where teacher_subjectteacher_id = %s and teacher_subjectclass_id = %s",
        [id,cl]

    )

    for obj in teachers:
        if obj.teacher_subjectcode not in listsel:
            response_data = {}

            response_data['subjectCode'] = obj.teacher_subjectcode
            response_data['subjectName'] = obj.subject_name

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)


def dynamicaddress(request):
    response_data = {}
    response_data['url'] = urlsplit(
        request.build_absolute_uri(None)).scheme + '://' + request.get_host() + '/static/img/spinner.gif'
    return JsonResponse(response_data)


def assignsubjects(request):
    subject = request.POST.get('subjects', None)
    teacher = request.POST.get('teacher', None)
    classes = request.POST.get('classcode', None)
    unstringified = json.loads(subject)

    for std in unstringified:
        print(std)
        teachers = Teachers.objects.get(pk=teacher)
        subjects = Subjects.objects.get(pk=std)
        clss = SchoolClasses.objects.get(pk=classes)
        teacherSubjects = TeacherSubjects()
        teacherSubjects.teacher_subjectsubject = subjects
        teacherSubjects.teacher_subjectteacher = teachers
        teacherSubjects.teacher_subjectclass = clss

        assn = TeacherSubjects.objects.filter(teacher_subjectsubject=subjects,
                                              teacher_subjectclass=clss).exists()
        if (assn):
            return JsonResponse({'error':subjects.subject_name + ' already assigned'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            teacherSubjects.save()

        # try:
        #     subjecttea = TeacherSubjects.objects.get(teacher_subjectsubject=subjects,teacher_subjectclass=clss)
        # except TeacherSubjects.DoesNotExist:
        #        teacherSubjects.save()

    return JsonResponse({'success': 'Assigned Successfully'})


def unassignsubjects(request):
    students = request.POST.get('subjects', None)
    unstringified = json.loads(students)

    for std in unstringified:
        print(std)
        studSubjects = TeacherSubjects.objects.get(pk=std)
        studSubjects.delete()

    return JsonResponse({'success': 'Unassigned Successfully'})

def assignallsubjects(request):
    teacher = request.POST.get('teacher', None)
    classes = request.POST.get('classcode', None)
    teachers = Teachers.objects.get(pk=teacher)
    clss = SchoolClasses.objects.get(pk=classes)

    subjects = Subjects.objects.all()
    for obj in subjects:

        std = obj.subject_code
        sub=Subjects.objects.get(pk=std)

        teachersubjects = TeacherSubjects()
        teachersubjects.teacher_subjectteacher = teachers
        teachersubjects.teacher_subjectsubject = sub
        teachersubjects.teacher_subjectclass = clss

        assn=TeacherSubjects.objects.filter(teacher_subjectsubject=sub,
                                    teacher_subjectclass=clss).exists()
        if(assn):
            return JsonResponse({'error': sub.subject_name +' already assigned'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            teachersubjects.save()

        # try:
        #     subjecttea = TeacherSubjects.objects.get(teacher_subjectteacher=teachers,teacher_subjectsubject=sub,teacher_subjectclass=clss)
        # except TeacherSubjects.DoesNotExist:
        #        teachersubjects.save()

    return JsonResponse({'success': 'Unassigned Successfully'})


def unassignallsubjects(request):
    teacher = request.POST.get('teacher', None)
    classes = request.POST.get('classcode', None)
    teachers = TeacherSubjects.objects.raw("select teacher_subjectcode from teachersubjects_teachersubjects where teacher_subjectteacher_id =%s and teacher_subjectclass_id =%s",[teacher,classes])
    for obj in teachers:
        std=obj.teacher_subjectcode
        try:
            subject = TeacherSubjects.objects.get(pk=std)
            subject.delete()
        except TeacherSubjects.DoesNotExist:
            return JsonResponse({'error': 'Subject doesnt exist'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse({'success': 'Unassigned Successfully'})


def transfersubjects(request):
    teacherFrom = request.POST.get('transferFrom', None)
    teacherTo = request.POST.get('transferTo', None)

    teachersTo = Teachers.objects.get(pk=teacherTo)

    teachersubs = TeacherSubjects.objects.raw("select teacher_subjectcode from teachersubjects_teachersubjects where teacher_subjectteacher_id =%s",[teacherFrom])
    for obj in teachersubs:

        teachersubjects = TeacherSubjects()
        teachersubjects.teacher_subjectteacher = teachersTo
        teachersubjects.teacher_subjectsubject = obj.teacher_subjectsubject
        try:
            subjecttea = TeacherSubjects.objects.get(teacher_subjectteacher=teachersTo,teacher_subjectsubject=obj.teacher_subjectsubject)
        except TeacherSubjects.DoesNotExist:
               teachersubjects.save()

    teachersubs2 = TeacherSubjects.objects.raw("select teacher_subjectcode from teachersubjects_teachersubjects where teacher_subjectteacher_id =%s",[teacherFrom])
    for obj in teachersubs2:
        try:
            subject = TeacherSubjects.objects.get(pk=obj.teacher_subjectcode)
            subject.delete()
        except TeacherSubjects.DoesNotExist:
            return JsonResponse({'error': 'Subject doesnt exist'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse({'success': 'Transferred Successfully'})


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