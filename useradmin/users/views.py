from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_control

from staff.teachers.models import Teachers
from localities.models import Select2Data
from localities.serializers import Select2Serializer
from useradmin.users.forms import UserForm
from useradmin.users.models import UserType, User


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def userreg(request):
    return render(request, 'users/user.html')


def createuser(request):
    active=''
    if request.method == 'POST' and 'user_active' in request.POST:
        val = request.POST['user_active']
        active = val
    else:
        t_ref = None
    if request.method == 'POST' and 'user_teacher_ref' in request.POST:
        val = request.POST['user_teacher_ref']
        t_ref = val
    else:
        t_ref = None
    users = UserForm(request.POST)
    print(users.data["username"])
    userType = users.data['user_type']
    userSupervisor = users.data['user_supervisor']

    if userType is not None and userType != '':
        ut = UserType.objects.get(pk=userType)
        users.user_type=ut
    else:
        users.user_type = None

    if userSupervisor is not None and userSupervisor != '':
        us = User.objects.get(pk=userSupervisor)
        users.user_supervisor = us
    else:
        users.user_supervisor = None

    if active is not None and active == 'on':
        users.user_active = True
    else:
        users.user_active = False

    user=User.objects.create_user(users.data["username"],users.data["password"],users.data["user_firstname"],users.data["user_lastname"],users.data["email"],
                                  users.data["user_phone"],users.data["user_address"],users.data["user_gender"],users.user_active,t_ref,users.user_type,users.user_supervisor)
    return JsonResponse({'success': 'User Saved Successfully'})




def searchtypes(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    types = UserType.objects.raw(
        "SELECT top 5 type_code,type_name FROM users_usertype WHERE type_name like %s or type_desc like %s",
        tuple([query, query]))

    for obj in types:
        select2 = Select2Data()
        select2.id = str(obj.type_code)
        select2.text = obj.type_name
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchsupervisor(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    users = User.objects.raw(
        "SELECT top 5 user_id,concat(user_firstname,' ',user_lastname)name FROM users_user WHERE user_firstname like %s or user_lastname like %s or username like %s",
        [query, query,query])

    for obj in users:
        select2 = Select2Data()
        select2.id = str(obj.user_id)
        select2.text = obj.name
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchteachers(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    teachers = Teachers.objects.raw(
        "SELECT top 5 teacher_code,teacher_name FROM teachers_teachers WHERE teacher_name like %s or intials like %s",
        tuple([query, query]))

    for obj in teachers:
        select2 = Select2Data()
        select2.id = str(obj.teacher_code)
        select2.text = obj.teacher_name
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def updateuser(request,id):
    active = False
    if request.method == 'POST' and 'user_active' in request.POST:
        val = request.POST['user_active']
        if val == 'on':
           active = True
    else:
        active = False

    userId=request.POST.get('user_id')
    userId=int(userId)


    users = User.objects.get(pk=userId)
    users.user_id=userId
    users.user_phone=request.POST.get('user_phone',None)
    users.user_firstname = request.POST.get('user_firstname',None)
    users.user_lastname=request.POST.get('user_lastname',None)
    users.user_address = request.POST.get('user_address',None)
    users.user_teacher_ref = request.POST.get('user_teacher_ref',None)
    users.is_active=active
    users.user_gender = request.POST.get('user_gender',None)
    user_type=request.POST.get('user_type',None)
    users.email=request.POST.get('email',None)

    user_sup=request.POST.get('user_supervisor',None)


    if user_type is not None and user_type != '':
        ut = UserType.objects.get(pk=user_type)
        users.user_type=ut
    else:
        users.user_type = None

    if user_sup is not None and user_sup != '':
        us = User.objects.get(pk=user_sup)
        users.user_supervisor = us
    else:
        users.user_sup = None


    users.save()
    return JsonResponse({'success': 'User Updated Successfully'})


def getusers(request):
    listsel = []
    users = User.objects.raw(
        "SELECT DISTINCT u.user_id,u.is_active,u.email,u.username as userName,u.user_firstname as userFname,u.user_lastname as userLname,u.user_address as userAddress,u.user_gender as userGender,u.user_phone as userPhone,type_name as userType,v.username as supervisorName FROM users_user u" +
        " LEFT JOIN  users_user v ON u.user_supervisor_id=v.user_id" +
        " LEFT JOIN users_usertype s ON u.user_type_id=s.type_code")

    for obj in users:
        if obj.user_id not in listsel:
            response_data = {}
            response_data['userId'] = obj.user_id
            response_data['email'] = obj.email
            response_data['status'] = obj.is_active
            response_data['userName'] = obj.userName
            response_data['userFname'] = obj.userFname
            response_data['userLname'] = obj.userLname
            response_data['userAddress'] = obj.userAddress
            response_data['userPhone'] = obj.userPhone
            response_data['userType'] = obj.userType
            response_data['supervisorName'] = obj.supervisorName
            if obj.supervisorName is None:
                response_data['supervisorName'] = "No Supervisor"
            else:
                response_data['supervisorName'] = obj.supervisorName

            if obj.userGender is not None:
                if obj.userGender == 'F':
                   response_data['userGender'] = "Female"
                elif obj.userGender == 'M':
                   response_data['userGender'] = "Male"
                else:
                    response_data['userGender'] = "Other"
            else:
                response_data['userGender'] = "Not Availed"

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)

def edituser(request,id):
    users = User.objects.get(pk=id)
    response_data = {}
    if users.user_type is not None:
        userType = UserType.objects.get(pk=users.user_type.pk)
        response_data['userTypeCode'] = userType.type_code
        response_data['userTypeName'] = userType.type_desc
    if users.user_supervisor is not None:
        supervisor = User.objects.get(pk=users.user_supervisor.pk)
        response_data['supervisorCode'] = supervisor.user_id
        response_data['supervisorName'] = supervisor.user_firstname+' '+supervisor.user_lastname
    if users.user_teacher_ref is not None:
        teacher = Teachers.objects.raw("select teacher_code,teacher_name from teachers_teachers where teacher_code=%s",[users.user_teacher_ref])
        for obj in teacher:
           response_data['teacherCode']= obj.teacher_code
           response_data['teacherName'] = obj.teacher_name

    response_data['userId'] = users.user_id
    response_data['email'] = users.email
    response_data['status'] = users.is_active
    response_data['userName'] = users.username
    response_data['userFname'] = users.user_firstname
    response_data['userLname'] = users.user_lastname
    response_data['userAddress'] = users.user_address
    response_data['userPhone'] = users.user_phone
    response_data['userGender'] = users.user_gender

    return JsonResponse(response_data)


def deleteuser(request,id):
    user=User.objects.get(pk=id)
    user.delete()
    return JsonResponse({'success': 'User Deleted Successfully'})
