import json
from urllib.parse import urlsplit

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from localities.models import Select2Data
from localities.serializers import Select2Serializer
from setups.academics.classes.models import SchoolClasses
from studentmanager.student.models import Students
from studentmanager.studentleaveouts.models import Leaveouts
from studentmanager.studentsubjects.models import StudentSubjects
from useradmin.users.models import User


def leaveoutspage(request):
    context={}
    if request.method == 'GET' and 'student' in request.GET:
        context = {
            'student': request.GET['student']
        }
    else:
        context = {
            'student': 'None'
        }

    return render(request,'students/studentleaveouts.html',context)


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

def getunassignedstudents(request,id):
    listsel = []
    students = Students.objects.raw(
        "SELECT student_code,concat(adm_no,'--',student_name)name FROM student_students" +
        " where student_class_id = %s and student_school_status='Active'",
        [id]

    )

    for obj in students:
        if obj.student_code not in listsel:
            response_data = {}

            response_data['studentCode'] = obj.student_code
            response_data['name'] = obj.name

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)

def getassignedleavestudents(request,id):
    listsel = []
    students = Leaveouts.objects.raw(
        "SELECT leave_code,student_code,concat(adm_no,'--',student_name)name,class_name,class_code FROM studentleaveouts_leaveouts" +
        " inner join student_students  on student_code = leave_student_id"+
        " inner join classes_schoolclasses  on class_code = student_class_id" +
        " where student_class_id = %s and leave_returned='N'",
        [id]

    )

    for obj in students:
        if obj.student_code not in listsel:
            response_data = {}

            response_data['studentCode'] = obj.leave_code
            response_data['name'] = obj.name
            response_data['class_name'] = obj.class_name
            response_data['class_code'] = obj.class_code


            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)

def getindividualstudent(request,id):
    listsel = []
    students = Students.objects.raw(
        "SELECT student_code,concat(adm_no,'--',student_name)name,class_name,class_code FROM student_students"+
        " inner join classes_schoolclasses on student_class_id = class_code" +
        " where student_code = %s and student_school_status='Active'",
        [id]

    )

    for obj in students:
        if obj.student_code not in listsel:
            response_data = {}

            response_data['studentCode'] = obj.student_code
            response_data['name'] = obj.name
            response_data['class_name']=obj.class_name
            response_data['class_code']=obj.class_code

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)




def getindividualleavestudent(request,id):
    listsel = []
    students = Leaveouts.objects.raw(
        "SELECT leave_code,student_code,leave_reason,date_left,date_expected_back,concat(adm_no,'--',student_name)name,class_name,class_code FROM studentleaveouts_leaveouts" +
        " inner join student_students  on student_code = leave_student_id"+
        " inner join classes_schoolclasses  on class_code = student_class_id" +
        " where student_code = %s and leave_returned='N'",
        [id]

    )

    for obj in students:
        if obj.student_code not in listsel:
            response_data = {}

            response_data['studentCode'] = obj.leave_code
            response_data['name'] = obj.name
            response_data['class_name'] = obj.class_name
            response_data['class_code'] = obj.class_code
            response_data['reason'] = obj.leave_reason
            response_data['date_left'] = obj.date_left.strftime("%Y-%m-%d")
            response_data['date_expected_back'] = obj.date_expected_back.strftime("%Y-%m-%d")

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)


def dynamicaddress(request):
    response_data = {}
    response_data['url'] = urlsplit(
        request.build_absolute_uri(None)).scheme + '://' + request.get_host() + '/static/img/spinner.gif'
    return JsonResponse(response_data)


def assignleaveouts(request):
    students = request.POST.get('students', None)
    type = request.POST.get('type', None)
    classcode = request.POST.get('classcode', None)
    leftdate = request.POST.get('leftdate', None)
    returndate = request.POST.get('returndate', None)
    reason = request.POST.get('reason', None)
    returneddate = request.POST.get('returneddate', None)
    unstringified = json.loads(students)
    u = User.objects.get(username=request.user)
    response_data = {}
    for std in unstringified:
        leaveouts = Leaveouts()
        student = Students.objects.get(pk=std)
        classcodes = SchoolClasses.objects.get(pk=classcode)
        leaveouts.date_expected_back=returndate
        leaveouts.leave_reason=reason
        leaveouts.leave_student=student
        leaveouts.date_left=leftdate
        leaveouts.leave_class=classcodes
        leaveouts.user_leaveauthoriser=u
        leaveouts.leave_returned='N'
        leaveouts.save()
        student.student_school_status='Leave'
        student.save()
        response_data['code']=std

    response_data['success'] = 'Assigned Successfully'
    return JsonResponse(response_data)


def unassignleaveouts(request):
    students = request.POST.get('students', None)
    # type = request.POST.get('type', None)
    # classcode = request.POST.get('classcode', None)
    # leftdate = request.POST.get('leftdate', None)
    # returndate = request.POST.get('returndate', None)
    # reason = request.POST.get('reason', None)
    returneddate = request.POST.get('returneddate', None)
    unstringified = json.loads(students)
    u = User.objects.get(username=request.user)
    response_data = {}
    for std in unstringified:
        student = Leaveouts.objects.get(pk=std)
        student.date_returned=returneddate
        student.leave_returned='Y'
        student.user_returnauthoriser=u
        student.save()
        stud=Students.objects.get(pk=student.leave_student.pk)
        stud.student_school_status='Active'
        stud.save()
        response_data['code']=stud.pk

    response_data['success']='Assigned Successfully'
    return JsonResponse(response_data)


def unassignbulkleaves(request):
    students = request.POST.get('students', None)
    # type = request.POST.get('type', None)
    # classcode = request.POST.get('classcode', None)
    # leftdate = request.POST.get('leftdate', None)
    # returndate = request.POST.get('returndate', None)
    # reason = request.POST.get('reason', None)
    returneddate = request.POST.get('returneddate', None)
    unstringified = json.loads(students)
    response_data = {}
    for std in unstringified:
        student = Leaveouts.objects.get(pk=std)
        u = User.objects.get(username=request.user)
        student.date_returned = returneddate
        student.leave_returned = 'Y'
        student.user_returnauthoriser = u
        student.save()
        stud = Students.objects.get(pk=student.leave_student.pk)
        stud.student_school_status = 'Active'
        stud.save()

    response_data['success'] = 'Assigned Successfully'
    return JsonResponse(response_data)


def assignbulkleaves(request):
    students = request.POST.get('students', None)
    type = request.POST.get('type', None)
    classcode = request.POST.get('classcode', None)
    leftdate = request.POST.get('leftdate', None)
    returndate = request.POST.get('returndate', None)
    reason = request.POST.get('reason', None)
    returneddate = request.POST.get('returneddate', None)
    unstringified = json.loads(students)
    response_data = {}
    for std in unstringified:
        leaveouts = Leaveouts()
        student = Students.objects.get(pk=std)
        classcodes = SchoolClasses.objects.get(pk=classcode)
        u = User.objects.get(username=request.user)
        leaveouts.date_expected_back = returndate
        leaveouts.leave_reason = reason
        leaveouts.leave_student = student
        leaveouts.date_left = leftdate
        leaveouts.leave_class = classcodes
        leaveouts.user_leaveauthoriser = u
        leaveouts.leave_returned = 'N'
        leaveouts.save()
        student.student_school_status = 'Leave'
        student.save()

    response_data['success'] = 'Assigned Successfully'
    return JsonResponse(response_data)


def unassignallleaveouts(request):

    returneddate = request.POST.get('returneddate', None)
    classcode = request.POST.get('classcode', None)
    students = Leaveouts.objects.raw("select leave_code from studentleaveouts_leaveouts where leave_class_id =%s and leave_returned='N'", [classcode])
    response_data = {}
    for std in students:
        student = Leaveouts.objects.get(pk=std.leave_code)
        u = User.objects.get(username=request.user)
        student.date_returned = returneddate
        student.leave_returned = 'Y'
        student.user_returnauthoriser = u
        student.save()
        stud = Students.objects.get(pk=student.leave_student.pk)
        stud.student_school_status = 'Active'
        stud.save()

    response_data['success'] = 'Assigned Successfully'
    return JsonResponse(response_data)


def assignallleaveouts(request):
    type = request.POST.get('type', None)
    classcode = request.POST.get('classcode', None)
    leftdate = request.POST.get('leftdate', None)
    returndate = request.POST.get('returndate', None)
    reason = request.POST.get('reason', None)
    returneddate = request.POST.get('returneddate', None)
    students = Students.objects.raw("select student_code from student_students where student_class_id =%s and student_school_status='Active'", [classcode])
    response_data = {}
    for std in students:
        print(std)
        leaveouts = Leaveouts()
        student = Students.objects.get(pk=std.student_code)
        classcodes = SchoolClasses.objects.get(pk=classcode)
        u = User.objects.get(username=request.user)
        leaveouts.date_expected_back = returndate
        leaveouts.leave_reason = reason
        leaveouts.leave_student = student
        leaveouts.date_left = leftdate
        leaveouts.leave_class = classcodes
        leaveouts.user_leaveauthoriser = u
        leaveouts.leave_returned = 'N'
        leaveouts.save()
        student.student_school_status = 'Leave'
        student.save()

    response_data['success'] = 'Assigned Successfully'
    return JsonResponse(response_data)


def getstudentsleaves(request):
    listsel = []
    students = Leaveouts.objects.raw(
        "SELECT top 50 leave_code,student_code,adm_no,student_name,leave_reason,date_left,date_expected_back," +
        "class_name,l.username as authorised_by,r.username as returned_by,leave_returned,date_returned FROM studentleaveouts_leaveouts" +
        " inner join student_students  on student_code = leave_student_id" +
        " inner join classes_schoolclasses  on class_code = leave_class_id" +
        " left join users_user l on user_leaveauthoriser_id = l.user_id" +
        " left join users_user r on user_returnauthoriser_id = r.user_id"

    )

    for obj in students:
        if obj.student_code not in listsel:
            response_data = {}

            response_data['studentCode'] = obj.student_code
            response_data['leaveCode'] = obj.leave_code

            response_data['name'] = obj.student_name
            response_data['admNo'] = obj.adm_no
            response_data['dateLeft'] = obj.date_left.strftime("%d/%m/%Y")
            response_data['dateExpected'] = obj.date_expected_back.strftime("%d/%m/%Y")
            response_data['reason'] = obj.leave_reason
            response_data['studentClass'] = obj.class_name
            response_data['authorisedBy'] = obj.authorised_by
            response_data['returnedBy'] = obj.returned_by
            if obj.date_returned:
                response_data['dateReturned'] = obj.date_returned.strftime("%d/%m/%Y")
            else:
                response_data['dateReturned'] = ''

            if obj.leave_returned == 'N':
                response_data['returned'] = "No"
            elif obj.leave_returned == 'Y':
                response_data['returned'] = "Yes"
            else:
                response_data['returned'] = "No"

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)

def editstudent(request,id):
    listsel = []
    students = Leaveouts.objects.raw(
        "SELECT top 50 leave_code,leave_student_id,leave_reason,date_left,date_expected_back," +
        "leave_returned,date_returned FROM studentleaveouts_leaveouts" +
        " where leave_code = %s",[id]

    )

    for obj in students:
            response_data = {}

            response_data['leaveCode'] = obj.leave_code
            response_data['studentCode'] = obj.leave_student_id
            response_data['dateLeft'] = obj.date_left.strftime("%Y-%m-%d")
            response_data['dateExpected'] = obj.date_expected_back.strftime("%Y-%m-%d")
            response_data['reason'] = obj.leave_reason

            if obj.date_returned:
                response_data['dateReturned'] = obj.date_returned.strftime("%Y-%m-%d")
            if obj.leave_returned == 'N':
                response_data['returned'] = "No"
            elif obj.leave_returned == 'Y':
                response_data['returned'] = "Yes"
            else:
                response_data['returned'] = "No"

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)