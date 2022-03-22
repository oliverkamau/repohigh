from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_control
from rest_framework import status

from localities.models import Select2Data
from localities.serializers import Select2Serializer
from setups.academics.classes.models import SchoolClasses
from setups.academics.classsubjects.models import ClassSubjects
from setups.academics.subjects.models import Subjects
from setups.academics.termdates.models import TermDates
from staff.teachers.models import Teachers
from staff.teachersubjects.models import TeacherSubjects
from timetabling.daysetups.models import DaySetups
from timetabling.lessonallocation.forms import LessonAllocationForm
from timetabling.lessonallocation.models import LessonAllocation
from timetabling.lessonsetups.models import LessonSetups


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def lessonallocation(request):
    return render(request, 'timetabling/lessonallocation.html')


def searchclasses(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    classes = SchoolClasses.objects.raw(
        "SELECT top 5 class_code,class_name FROM classes_schoolclasses WHERE class_name like %s",
       [query])

    for obj in classes:
        text = obj.class_name
        select2 = Select2Data()
        select2.id = str(obj.class_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchdays(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    days = DaySetups.objects.raw(
        "SELECT top 5 day_code,day_name FROM daysetups_daysetups WHERE day_name like %s",
        [query])

    for obj in days:
        text = obj.day_name
        select2 = Select2Data()
        select2.id = str(obj.day_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchlessons(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    lessons = LessonSetups.objects.raw(
        "SELECT top 5 lesson_code,lesson_name FROM lessonsetups_lessonsetups WHERE lesson_type = 'L' and lesson_name like %s",
        [query])

    for obj in lessons:
        text = obj.lesson_name
        select2 = Select2Data()
        select2.id = str(obj.lesson_code)
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


def searchsubjects(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    subjects = Subjects.objects.raw(
        "SELECT top 5 subject_code,subject_name from subjects_subjects where subject_name like %s",
        [query])

    for obj in subjects:
        text = obj.subject_name
        select2 = Select2Data()
        select2.id = str(obj.subject_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def getcurrentterm(request):
    response_data = {}
    obj = TermDates.objects.get(current_term=True)
    response_data['termCode'] = obj.term_code
    response_data['termNumber'] = obj.term_number
    return JsonResponse(response_data)


def getTimetable(request):

  listsel = []
  tables = LessonAllocation.objects.raw(
    "select timetable_code,lesson_name,subject_name,day_name,class_name,term_number,teacher_name"+
    " from lessonallocation_lessonallocation"+
    " left join lessonsetups_lessonsetups on timetable_lesson_id = lesson_code"+
    " left join daysetups_daysetups on timetable_day_id = day_code"+
    " left join classes_schoolclasses on timetable_class_id = class_code"
    " left join subjects_subjects on timetable_subject_id = subject_code" +
    " left join teachers_teachers on timetable_teacher_id = teacher_code" +
    " left join termdates_termdates on timetable_term_id = term_code")

  for obj in tables:
    if obj.timetable_code not in listsel:
        response_data = {}
        response_data['code'] = obj.timetable_code
        response_data['lessonName'] = obj.lesson_name
        response_data['dayName'] = obj.day_name
        response_data['subjectName'] = obj.subject_name
        response_data['teacherName'] = obj.teacher_name
        response_data['termName'] = obj.term_number
        response_data['className'] = obj.class_name


        listsel.append(response_data)

  return JsonResponse(listsel, safe=False)


def createtimetable(request):

    timetable = LessonAllocationForm(request.POST)
    td = timetable.data['timetable_day']
    tc = timetable.data['timetable_class']
    tl = timetable.data['timetable_lesson']
    tt = timetable.data['timetable_term']
    ts = timetable.data['timetable_subject']
    tts = timetable.data['timetable_teacher']
    timetabling = LessonAllocation()
    lesson = LessonSetups()
    classes = SchoolClasses()
    subject = Subjects()
    alloc = ClassSubjects()
    term = TermDates()

    if td is not None and td != '':
        day = DaySetups.objects.get(pk=td)
        timetabling.timetable_day = day

    if tc is not None and tc != '':
        classes = SchoolClasses.objects.get(pk=tc)
        timetabling.timetable_class = classes

    if tl is not None and tl != '':
        lesson = LessonSetups.objects.get(pk=tl)
        timetabling.timetable_lesson = lesson

    if tt is not None and tt != '':
        term = TermDates.objects.get(pk=tt)
        timetabling.timetable_term = term

    if ts is not None and ts != '':
        subject = Subjects.objects.get(pk=ts)
        timetabling.timetable_subject = subject

    if tts is not None and tts != '':
        teacher = Teachers.objects.get(pk=tts)
        timetabling.timetable_teacher = teacher


    try:
        alloc = ClassSubjects.objects.get(classsubject_subject=timetabling.timetable_subject, classsubject_class=timetabling.timetable_class)
    except alloc.DoesNotExist:
        return JsonResponse({'error': subject.subject_name + ' is not set for '+classes.class_name},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        num = alloc.lessons_perweek
        print('number allocated '+str(num))
        count = LessonAllocation.objects.filter(timetable_subject=timetabling.timetable_subject,
                                                timetable_class=timetabling.timetable_class,
                                                timetable_term=timetabling.timetable_term).count()
        print('Count for currently assigned '+str(count))
        if count <= num:

            cnt = LessonAllocation.objects.filter(timetable_day=timetabling.timetable_day,
                                                    timetable_subject=timetabling.timetable_subject,
                                                    timetable_class=timetabling.timetable_class).count()
            print('The count assigned currently for today is '+str(cnt))
            if cnt == 0:
                tcount = LessonAllocation.objects.filter(timetable_day=timetabling.timetable_day,
                                                         timetable_lesson=timetabling.timetable_lesson,
                                                         timetable_teacher=timetabling.timetable_teacher).count()
                print('The teacher assigned subject number is ' + str(tcount))
                if tcount == 0:

                    if alloc.stroked_subject:
                        stroked = alloc.stroked_with
                        strokedsubject = ClassSubjects.objects.filter(stroked_with=stroked,classsubject_class=classes)
                        if strokedsubject:
                            for stro in strokedsubject:
                                subj = Subjects.objects.get(pk=stro.classsubject_subject.pk)
                                print(subj.subject_name)
                                classstrk = SchoolClasses.objects.get(pk=stro.classsubject_class.pk)
                                teachersubject = TeacherSubjects()
                                try:
                                    teachersubject = TeacherSubjects.objects.get(teacher_subjectclass=classes,
                                                                             teacher_subjectsubject=subj)
                                    subjs = Subjects.objects.get(pk=teachersubject.teacher_subjectsubject.pk)
                                except teachersubject.DoesNotExist:
                                    delestroked = LessonAllocation.objects.filter(timetable_day=timetabling.timetable_day,
                                                                               timetable_lesson=timetabling.timetable_lesson,
                                                                               timetable_class=classstrk)
                                    if delestroked:
                                        for dele in delestroked:
                                            delesson = LessonAllocation.objects.get(pk=dele.timetable_code)
                                            delesson.delete()
                                    return JsonResponse(
                                        {'error': subj.subject_name + ' has no teacher assigned in ' + classes.class_name +' and it is stroked with '+subject.subject_name},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                                else:
                                     strteacher = Teachers.objects.get(pk=teachersubject.teacher_subjectteacher.pk)
                                     strcount = LessonAllocation.objects.filter(timetable_day=timetabling.timetable_day,
                                                                    timetable_lesson=timetabling.timetable_lesson,
                                                                    timetable_subject=subjs,
                                                                    timetable_teacher=strteacher).count()
                                     # print('Current count is '+str(strcount))
                                     if strcount == 0:
                                        checkdup = LessonAllocation()
                                        try:
                                            checkdup = LessonAllocation.objects.get(timetable_day=timetabling.timetable_day,
                                                     timetable_lesson=timetabling.timetable_lesson,timetable_subject=subj)
                                        except checkdup.DoesNotExist:
                                            strokedTable = LessonAllocation()
                                            strokedTable.timetable_lesson=timetabling.timetable_lesson
                                            strokedTable.timetable_day=timetabling.timetable_day
                                            strokedTable.timetable_subject=subj
                                            strokedTable.timetable_teacher=strteacher
                                            strokedTable.timetable_term=timetabling.timetable_term
                                            strokedTable.timetable_class=classstrk
                                            strokedTable.save()

                                     else :
                                        return JsonResponse(
                                           {'error': subj.subject_name + ' has the teacher assigned in another class at this lesson and its stroked with ' +subject.subject_name},
                                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        dup = LessonAllocation.objects.filter(timetable_day=timetabling.timetable_day,
                                                                timetable_lesson=timetabling.timetable_lesson,
                                                                   timetable_term=term).count()

                        if dup == 0:
                           timetabling.save()
                        else:
                           return JsonResponse({'error': 'Another lesson is already assigned in '+classes.class_name+' for '+lesson.lesson_name},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


                else:
                    return JsonResponse({'error': 'The teacher is already assigned to another lesson in another class'},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            elif cnt == 1:
                tcount = LessonAllocation.objects.filter(timetable_day=timetabling.timetable_day,
                                                         timetable_lesson=timetabling.timetable_lesson,
                                                         timetable_teacher=timetabling.timetable_teacher).count()
                if tcount == 0:

                    allocs = LessonAllocation.objects.get(timetable_day=timetabling.timetable_day,
                                                          timetable_subject=timetabling.timetable_subject,
                                                          timetable_class=timetabling.timetable_class)

                    less1 = LessonSetups.objects.get(pk=allocs.timetable_lesson.pk)
                    if less1.lesson_end == lesson.lesson_start:
                        if alloc.stroked_subject:
                            stroked = alloc.stroked_with
                            strokedsubject = ClassSubjects.objects.filter(stroked_with=stroked,
                                                                          classsubject_class=classes)
                            if strokedsubject:
                                for stro in strokedsubject:
                                    subj = Subjects.objects.get(pk=stro.classsubject_subject.pk)
                                    classstrk = SchoolClasses.objects.get(pk=stro.classsubject_class.pk)
                                    teachersubject = TeacherSubjects()
                                    try:
                                        teachersubject = TeacherSubjects.objects.get(teacher_subjectclass=classes,
                                                                                     teacher_subjectsubject=subj)
                                        subjs = Subjects.objects.get(pk=teachersubject.teacher_subjectsubject.pk)

                                    except teachersubject.DoesNotExist:
                                        delestroked = LessonAllocation.objects.filter(
                                            timetable_day=timetabling.timetable_day,
                                            timetable_lesson=timetabling.timetable_lesson,
                                            timetable_class=classstrk)
                                        if delestroked:
                                            for dele in delestroked:
                                                delesson = LessonAllocation.objects.get(pk=dele.timetable_code)
                                                delesson.delete()
                                        return JsonResponse(
                                            {
                                                'error': subj.subject_name + ' has no teacher assigned in ' + classes.class_name + ' and it is stroked with' + subject.subject_name},
                                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                                    else:
                                        strteacher = Teachers.objects.get(pk=teachersubject.teacher_subjectteacher.pk)
                                        strcount = LessonAllocation.objects.filter(
                                            timetable_day=timetabling.timetable_day,
                                            timetable_lesson=timetabling.timetable_lesson,
                                            timetable_subject=subjs,
                                            timetable_teacher=strteacher).count()
                                    if strcount == 0:
                                        checkdup = LessonAllocation()
                                        try:
                                            checkdup = LessonAllocation.objects.get(
                                                timetable_day=timetabling.timetable_day,
                                                timetable_lesson=timetabling.timetable_lesson, timetable_subject=subj)
                                        except checkdup.DoesNotExist:
                                            strokedTable = LessonAllocation()
                                            strokedTable.timetable_lesson = timetabling.timetable_lesson
                                            strokedTable.timetable_day = timetabling.timetable_day
                                            strokedTable.timetable_subject = subj
                                            strokedTable.timetable_teacher = strteacher
                                            strokedTable.timetable_term = timetabling.timetable_term
                                            strokedTable.timetable_class = classstrk
                                            strokedTable.save()

                                    else:
                                        return JsonResponse(
                                            {
                                                'error': subj.subject_name + ' has the teacher assigned in another class at this lesson and its stroked with ' + subject.subject_name},
                                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        else:
                            timetabling.save()
                    else:
                        return JsonResponse(
                            {'error': 'Double lessons should not have a break or a lesson between them'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return JsonResponse({'error': 'The teacher is already assigned to another lesson in another class'},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            elif count > 1:
                return JsonResponse(
                    {'error': 'This lesson already has a double today so its not possible to have it again'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            print(count)
            # timetable.save()


        else:
            return JsonResponse({'error': 'You can only have '+str(num)+' '+subject.subject_name + ' lessons per week!'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    return JsonResponse({'success': 'Timetable Saved Successfully'})


def updatetimetable(request):
    return None


def getteacher(request,classcodes,subject):
    classcode = SchoolClasses.objects.get(pk=classcodes)
    subjects = Subjects.objects.get(pk=subject)
    resp = {}
    teachers = TeacherSubjects();
    try:
        teachers = TeacherSubjects.objects.get(teacher_subjectclass=classcode, teacher_subjectsubject=subjects)
        teacher = Teachers.objects.get(pk=teachers.teacher_subjectteacher.pk)
        resp['teacherName'] = teacher.teacher_name
        resp['teacherCode'] = teacher.teacher_code
    except teachers.DoesNotExist:
        resp['teacherName'] = ''
        resp['teacherCode'] = ''


    return JsonResponse(resp)

