from datetime import datetime
import json
from urllib.parse import urlsplit

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_control

from localities.models import Select2Data
from localities.serializers import Select2Serializer
from setups.academics.classes.models import SchoolClasses
from studentmanager.student.models import Students


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def studentmovements(request):
    return render(request,'students/studentmovement.html')

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


def searchstudent(request,id):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    students = Students.objects.raw(
        "SELECT top 5 student_code,concat(adm_no,'--',student_name)name FROM student_students WHERE student_class_id=%s and( adm_no like %s or student_name like %s)",
        [id,query, query])

    for obj in students:
        text = obj.name
        select2 = Select2Data()
        select2.id = str(obj.student_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def getstudents(request):
    listsel = []
    students = Students.objects.raw(
        "SELECT top 100 student_code,student_school_status,adm_no,student_name,date_of_birth,adm_date,completion_date,dorm_name," +
        "class_name,student_email,student_phone,coalesce(father_name,mother_name)parent,student_gender,country_name FROM student_students" +
        " LEFT JOIN dorms_dorms ON student_dorm_id=dorm_code" +
        " LEFT JOIN classes_schoolclasses ON student_class_id=class_code" +
        " LEFT JOIN localities_countries ON nationality_id=country_id" +
        " LEFT JOIN parents_parents ON student_parent_id=parent_code"

    )

    for obj in students:
        if obj.student_code not in listsel:
            response_data = {}

            response_data['studentCode'] = obj.student_code
            response_data['name'] = obj.student_name
            response_data['status'] = obj.student_school_status
            response_data['admNo'] = obj.adm_no
            response_data['birthDate'] = obj.date_of_birth.strftime("%d/%m/%Y")
            response_data['admDate'] = obj.adm_date.strftime("%d/%m/%Y")
            response_data['completionDate'] = obj.completion_date.strftime("%d/%m/%Y")
            response_data['dorm'] = obj.dorm_name
            response_data['studentClass'] = obj.class_name
            response_data['email'] = obj.student_email
            response_data['phone'] = obj.student_phone
            response_data['parent'] = obj.parent
            response_data['nationality'] = obj.country_name

            if obj.student_gender == 'M':
                response_data['gender'] = "Male"
            elif obj.student_gender == 'F':
                response_data['gender'] = "Female"
            else:
                response_data['gender'] = "Other"

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)

def getunassignedstudents(request,id):
    listsel = []
    students = Students.objects.raw(
        "SELECT student_code,concat(adm_no,'--',student_name)name FROM student_students" +
        " where student_class_id = %s",
        [id]

    )

    for obj in students:
        if obj.student_code not in listsel:
            response_data = {}

            response_data['studentCode'] = obj.student_code
            response_data['name'] = obj.name

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)

def getassignedstudents(request,id):
    listsel = []
    students = Students.objects.raw(
        "SELECT student_code,concat(adm_no,'--',student_name)name FROM student_students" +
        " where student_school_status='Active' and  student_class_id = %s",
        [id]

    )

    for obj in students:
        if obj.student_code not in listsel:
            response_data = {}

            response_data['studentCode'] = obj.student_code
            response_data['name'] = obj.name

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)

def dynamicaddress(request):
    response_data = {}
    response_data['url'] = urlsplit(
        request.build_absolute_uri(None)).scheme + '://' + request.get_host() + '/static/img/spinner.gif'
    return JsonResponse(response_data)

def studentmovement(request):
    classcode = request.POST.get('movement_class', None)
    student = request.POST.get('movement_student', None)
    action = request.POST.get('movement_action', None)
    term = request.POST.get('movement_term', None)
    date = request.POST.get('movement_date', None)
    resume = request.POST.get('resume_date', None)
    reason = request.POST.get('movement_reason', None)
    print(date)
    print(resume)
    todo=''
    if(action=='EX'):
        todo='Expelled'
    elif(action=='ES'):
        todo='Active'
    elif(action=='S'):
        todo = 'Suspended'
    elif(action=='T'):
        todo = 'Transferred'
    else:
        todo = None

    if(todo=='Expelled' or todo=='Transferred'):
        student = Students.objects.get(pk=student)
        student.student_statuschange_date = date
        student.student_school_status = todo
        student.student_statuschange_reason = reason
        student.student_statuschange_term = term
        student.save()
    elif(todo=='Active' or todo=='Suspended'):
       student=Students.objects.get(pk=student)
       student.student_statuschange_date=date
       student.student_school_status=todo
       student.student_statuschange_reason=reason
       student.student_statuschange_term=term
       student.student_resume_date=resume
       student.save()

    return  JsonResponse({'success': 'Student '+todo+' successfully'})


def assignstudents(request):
    students = request.POST.get('students', None)
    nextcode = request.POST.get('nextclasscode', None)
    classcode = request.POST.get('classcode', None)
    movementdate = request.POST.get('movementdate', None)
    reason = request.POST.get('reason', None)
    term = request.POST.get('term',None)
    unstringified = json.loads(students)

    for std in unstringified:
        # print(std)
        student = Students.objects.get(pk=std)
        classcodes = SchoolClasses.objects.get(pk=classcode)
        nextcodes = SchoolClasses.objects.get(pk=nextcode)
        student.student_class=nextcodes
        student.student_statuschange_reason=reason
        student.student_statuschange_term=term
        student.student_statuschange_date=movementdate
        if(classcodes==nextcodes and classcodes.next_class_id is None):
            student.student_statuschange_reason='Graduation'
            student.student_school_status='Graduated'
            studentyear = datetime.today().year
            year = str(studentyear)
            student.year_of_completion = year
            student.completion_date = movementdate
        else:
            student.student_school_status='Active'

        student.save()
    return JsonResponse({'success': 'Moved Successfully'})


def unassignstudents(request):
    students = request.POST.get('students', None)
    classcode = request.POST.get('nextclasscode', None)
    nextcode = request.POST.get('classcode', None)
    movementdate = request.POST.get('movementdate', None)
    reason = request.POST.get('reason', None)
    term = request.POST.get('term', None)
    unstringified = json.loads(students)

    for std in unstringified:
        print(std)
        student = Students.objects.get(pk=std)
        classcodes = SchoolClasses.objects.get(pk=classcode)
        nextcodes = SchoolClasses.objects.get(pk=nextcode)
        student.student_class = nextcodes
        student.student_statuschange_reason = reason
        student.student_statuschange_term = term
        student.student_statuschange_date = movementdate
        if (classcodes == nextcodes and nextcodes.next_class_id is None):
            student.student_statuschange_reason = 'Graduation'
            student.student_school_status = 'Graduated'
            studentyear = datetime.today().year
            year = str(studentyear)
            student.year_of_completion = year
            student.completion_date = movementdate
        else:
            student.student_school_status = 'Active'

        student.save()
    return JsonResponse({'success': 'Moved Successfully'})


def assignallstudents(request):
    nextcode = request.POST.get('nextclasscode', None)
    classcode = request.POST.get('classcode', None)
    movementdate = request.POST.get('movementdate', None)
    reason = request.POST.get('reason', None)
    term = request.POST.get('term', None)
    students = Students.objects.raw(
        "select student_code from student_students where student_class_id =%s and student_school_status='Active'",
        [classcode])
    for std in students:

        print(std)
        student = Students.objects.get(pk=std.student_code)
        classcodes = SchoolClasses.objects.get(pk=classcode)
        nextcodes = SchoolClasses.objects.get(pk=nextcode)
        student.student_class = nextcodes
        student.student_statuschange_reason = reason
        student.student_statuschange_term = term
        student.student_statuschange_date = movementdate
        if (classcodes == nextcodes and classcodes.next_class_id is None):
            student.student_statuschange_reason = 'Graduation'
            student.student_school_status = 'Graduated'
            studentyear = datetime.today().year
            year = str(studentyear)
            student.year_of_completion = year
            student.completion_date = movementdate
        else:
            student.student_school_status = 'Active'

        student.save()

    return JsonResponse({'success': 'Unassigned Successfully'})


def unassignallstudents(request):
    classcode = request.POST.get('nextclasscode', None)
    nextcode = request.POST.get('classcode', None)
    movementdate = request.POST.get('movementdate', None)
    reason = request.POST.get('reason', None)
    term = request.POST.get('term', None)
    students = Students.objects.raw(
        "select student_code from student_students where student_class_id =%s and student_school_status='Active'",
        [classcode])
    for std in students:

        print(std)
        student = Students.objects.get(pk=std.student_code)
        classcodes = SchoolClasses.objects.get(pk=classcode)
        nextcodes = SchoolClasses.objects.get(pk=nextcode)
        student.student_class = nextcodes
        student.student_statuschange_reason = reason
        student.student_statuschange_term = term
        student.student_statuschange_date = movementdate
        if (classcodes == nextcodes and nextcodes.next_class_id is None):
            student.student_statuschange_reason = 'Graduation'
            student.student_school_status = 'Graduated'
            studentyear = datetime.today().year
            year=str(studentyear)
            student.year_of_completion=year
            student.completion_date=movementdate
        else:
            student.student_school_status = 'Active'

        student.save()

    return JsonResponse({'success': 'Unassigned Successfully'})


def getspecificstudents(request,action):
    todo = ''
    if (action == 'S'):
        todo = 'Suspended'
    elif (action == 'T'):
        todo = 'Transferred'
    elif (action == 'E'):
        todo = 'Expelled'
    elif (action == 'G'):
        todo = 'Graduated'

    listsel = []
    students = Students.objects.raw(
        'SELECT top 20 student_code,student_school_status,adm_no,student_name,date_of_birth,adm_date,completion_date,dorm_name,' +
        'class_name,student_email,student_phone,coalesce(father_name,mother_name)parent,student_gender,country_name FROM student_students' +
        ' LEFT JOIN dorms_dorms ON student_dorm_id=dorm_code' +
        ' LEFT JOIN classes_schoolclasses ON student_class_id=class_code' +
        ' LEFT JOIN localities_countries ON nationality_id=country_id' +
        ' LEFT JOIN parents_parents ON student_parent_id=parent_code' +
        ' where student_school_status=%s',
        [todo]

    )

    for obj in students:
        if obj.student_code not in listsel:
            response_data = {}

            response_data['studentCode'] = obj.student_code
            response_data['name'] = obj.student_name
            response_data['status'] = obj.student_school_status
            response_data['admNo'] = obj.adm_no
            response_data['birthDate'] = obj.date_of_birth.strftime("%d/%m/%Y")
            response_data['admDate'] = obj.adm_date.strftime("%d/%m/%Y")
            response_data['completionDate'] = obj.completion_date.strftime("%d/%m/%Y")
            response_data['dorm'] = obj.dorm_name
            response_data['studentClass'] = obj.class_name
            response_data['email'] = obj.student_email
            response_data['phone'] = obj.student_phone
            response_data['parent'] = obj.parent
            response_data['nationality'] = obj.country_name

            if obj.student_gender == 'M':
                response_data['gender'] = "Male"
            elif obj.student_gender == 'F':
                response_data['gender'] = "Female"
            else:
                response_data['gender'] = "Other"

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)


def getimage(request,id):
    response_data = {}
    student = Students.objects.get(pk=id)
    if(student.student_photo):
        response_data['url'] = urlsplit(
        request.build_absolute_uri(None)).scheme + '://' + request.get_host() + student.student_photo.url
    else:
        response_data['url'] =''
    return JsonResponse(response_data)


def editstudent(request,id):
    student = Students.objects.raw("select student_code,student_name,student_statuschange_term,student_statuschange_date," +
                                       "class_code,class_name,student_statuschange_reason,student_resume_date,student_school_status" +
                                       " from student_students" +
                                       " left join classes_schoolclasses on student_class_id = class_code" +
                                       " where student_code = %s", [id])
    listsel = []

    for obj in student:
            response_data = {}
            response_data['studentCode'] = obj.student_code
            response_data['studentName'] = obj.adm_no+'--'+obj.student_name
            response_data['term'] = obj.student_statuschange_term
            if obj.student_resume_date and obj.student_resume_date != '':
               response_data['resumeDate'] = obj.student_resume_date.strftime("%Y-%m-%d")
            if obj.student_statuschange_date and obj.student_statuschange_date != '':
               response_data['date'] = obj.student_statuschange_date.strftime("%Y-%m-%d")
            response_data['classCode'] = obj.class_code
            response_data['className'] = obj.class_name
            todo=''
            if (obj.student_school_status == 'Expelled'):
                todo = 'EX'
            elif (obj.student_school_status == 'Suspended'):
                todo = 'S'
            elif (obj.student_school_status == 'Transferred'):
                todo = 'T'
            else:
                todo = ""
            response_data['action'] = todo
            response_data['reason']= obj.student_statuschange_reason
            stud = Students.objects.get(pk=id)
            if stud.student_photo:
                response_data['url'] = urlsplit(
                    request.build_absolute_uri(None)).scheme + '://' + request.get_host() + stud.student_photo.url
            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)


def searchbyclass(request,id):

    listsel = []
    students = Students.objects.raw(
        "SELECT top 20 student_code,student_school_status,adm_no,student_name,date_of_birth,adm_date,completion_date,dorm_name," +
        "class_name,student_email,student_phone,coalesce(father_name,mother_name)parent,student_gender,country_name FROM student_students" +
        " LEFT JOIN dorms_dorms ON student_dorm_id=dorm_code" +
        " LEFT JOIN classes_schoolclasses ON student_class_id=class_code" +
        " LEFT JOIN localities_countries ON nationality_id=country_id" +
        " LEFT JOIN parents_parents ON student_parent_id=parent_code" +
        " where student_school_status='Active' and student_class_id = %s",
        [id]

    )

    for obj in students:
        if obj.student_code not in listsel:
            response_data = {}

            response_data['studentCode'] = obj.student_code
            response_data['name'] = obj.student_name
            response_data['status'] = obj.student_school_status
            response_data['admNo'] = obj.adm_no
            response_data['birthDate'] = obj.date_of_birth.strftime("%d/%m/%Y")
            response_data['admDate'] = obj.adm_date.strftime("%d/%m/%Y")
            response_data['completionDate'] = obj.completion_date.strftime("%d/%m/%Y")
            response_data['dorm'] = obj.dorm_name
            response_data['studentClass'] = obj.class_name
            response_data['email'] = obj.student_email
            response_data['phone'] = obj.student_phone
            response_data['parent'] = obj.parent
            response_data['nationality'] = obj.country_name

            if obj.student_gender == 'M':
                response_data['gender'] = "Male"
            elif obj.student_gender == 'F':
                response_data['gender'] = "Female"
            else:
                response_data['gender'] = "Other"

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)