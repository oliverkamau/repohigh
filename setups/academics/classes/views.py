from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_control

from setups.academics.classes.forms import ClassForm
from setups.academics.classes.models import SchoolClasses
from staff.teachers.models import Teachers
from students.models import Select2Data
from students.serializers import Select2Serializer

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def classes(request):
    return render(request, 'setups/academics/classes.html')


def createclass(request):
    active=''
    if request.method == 'POST' and 'active' in request.POST:
        val = request.POST['active']
        active = val
    else:
        active = ''
    schoolClass = ClassForm(request.POST)
    # tr = request.POST['class_teacher']
    tr = schoolClass.data['class_teacher']
    nx = schoolClass.data['next_class']
    # active = schoolClass.data['active']

    if tr is not None and tr != '':
        teacher = Teachers.objects.get(pk=tr)
        schoolClass.class_teacher=teacher
    if nx is not None and nx != '':
        nxtClass = SchoolClasses.objects.get(pk=nx)
        schoolClass.next_class = nxtClass

    if active is not None and active == 'on':
        schoolClass.active = True
    else:
        schoolClass.active = False

    schoolClass.save()
    return JsonResponse({'success': 'Class Saved Successfully'})

def getclasses(request):
    listsel = []
    classes = SchoolClasses.objects.raw(
        "SELECT DISTINCT v.class_code,v.class_name,v.active,v.max_capacity,teacher_name,s.class_name as nextClass FROM classes_schoolclasses v" +
        " LEFT JOIN  teachers_teachers ON v.class_teacher_id=teacher_code" +
        " LEFT JOIN classes_schoolclasses s ON v.next_class_id=s.class_code")


    for obj in classes:
        if obj.class_code not in listsel:
           response_data = {}
           response_data['classCode'] = obj.class_code
           if obj.nextClass is None:
              response_data['nextClass'] = "Not Set"
           else:
              response_data['nextClass'] = obj.nextClass

           if obj.teacher_name is None:
               response_data['classTeacher'] = "Not Availed"
           else:
               response_data['classTeacher'] = obj.teacher_name

           response_data['className'] = obj.class_name
           response_data['status'] = obj.active
           response_data['maxCapacity'] = obj.max_capacity
           response_data['currentCapacity'] = '0'

           listsel.append(response_data)


    return JsonResponse(listsel, safe=False)


def editclasses(request,id):
    classes = SchoolClasses.objects.get(pk=id)
    response_data = {}
    if classes.next_class is not None:
        nextClass = SchoolClasses.objects.get(pk=classes.next_class.pk)
        response_data['nextClassCode'] = nextClass.class_code
        response_data['nextClassName'] = nextClass.class_name
    if classes.class_teacher is not None:
        classTeacher = Teachers.objects.get(pk=classes.class_teacher.pk)
        response_data['classTeacherCode'] = classTeacher.teacher_code
        response_data['classTeacherName'] = classTeacher.teacher_name
    response_data['className'] = classes.class_name
    response_data['form'] = classes.form
    response_data['stream'] = classes.stream
    response_data['active'] = classes.active
    response_data['classCode'] = classes.class_code
    response_data['maxCapacity'] = classes.max_capacity
    response_data['currentCapacity'] = '0'
    response_data['admnoPrefix'] = classes.admno_prefix
    return JsonResponse(response_data)


def updateclasses(request,id):
    classes = SchoolClasses.objects.get(pk=id)
    form = ClassForm(request.POST, instance=classes)
    form.save()
    return JsonResponse({'success': 'Class Updated Successfully'})


def deleteclasses(request,id):
    classes = SchoolClasses.objects.get(pk=id)
    classes.delete()
    return JsonResponse({'success': 'Class Deleted Successfully'})


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


def searchclasses(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    classes = SchoolClasses.objects.raw(
        "SELECT top 5 class_code,class_name FROM classes_schoolclasses WHERE classes_schoolclasses.class_name like %s or classes_schoolclasses.form like %s",
        tuple([query, query]))

    for obj in classes:
        select2 = Select2Data()
        select2.id = str(obj.class_code)
        select2.text = obj.class_name
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})