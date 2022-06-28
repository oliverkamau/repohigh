from datetime import datetime
from io import BytesIO
from urllib.parse import urlsplit

import pandas as pd
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse, HttpResponse
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
from studentmanager.parents.models import Parents
from timetabling.daysetups.models import DaySetups
from timetabling.doublestracker.models import DoublesTracker
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

def dynamicspinneraddress(request):
    response_data = {}
    response_data['url'] = urlsplit(
        request.build_absolute_uri(None)).scheme + '://' + request.get_host() + '/static/img/spinner.gif'
    return JsonResponse(response_data)

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
                            {'error': 'Double lessons should not have a continue or a lesson between them'},
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
    teachers = TeacherSubjects()
    try:
        teachers = TeacherSubjects.objects.get(teacher_subjectclass=classcode, teacher_subjectsubject=subjects)
        teacher = Teachers.objects.get(pk=teachers.teacher_subjectteacher.pk)
        resp['teacherName'] = teacher.teacher_name
        resp['teacherCode'] = teacher.teacher_code
    except teachers.DoesNotExist:
        resp['teacherName'] = ''
        resp['teacherCode'] = ''


    return JsonResponse(resp)

def dynamicaddress(request):
    response_data = {}
    response_data['url'] = urlsplit(
        request.build_absolute_uri(None)).scheme + '://' + request.get_host()+'/'
    return JsonResponse(response_data)

def automatictimetable(request, alloc=None):

    days = DaySetups.objects.all()
    term = TermDates.objects.get(current_term=True)
    DoublesTracker.objects.filter(doubletracker_term=term).delete()
    LessonAllocation.objects.filter(timetable_term=term).delete()
    if days:
        for day in days:
            classes = SchoolClasses.objects.filter(active=True)
            if classes:
                for cls in classes:
                    allocs = ClassSubjects.objects.raw("select * from classsubjects_classsubjects" +
                                                       " inner join subjects_subjects ss on classsubjects_classsubjects.classsubject_subject_id = ss.subject_code" +
                                                       " inner join classes_schoolclasses cs on classsubjects_classsubjects.classsubject_class_id = cs.class_code" +
                                                       " where classsubject_class_id=%s"
                                                       " order by class_name,cast(subject_order as numeric)",
                                                       [cls.class_code])

                    if allocs:
                        for alloc in allocs:
                            print(alloc.subject_name)
                            lessons = LessonSetups.objects.raw("select * from lessonsetups_lessonsetups"
                                                               " where lesson_type='L'" +
                                                               " order by lesson_start")

                            if lessons:
                                for lesson in lessons:
                                    allocated = LessonAllocation.objects.filter(timetable_lesson=lesson,timetable_class=cls,timetable_term=term,
                                                                                timetable_day=day).count()
                                    if allocated == 0:
                                      num = alloc.lessons_perweek
                                      subject = Subjects.objects.get(pk=alloc.classsubject_subject.pk)
                                      count = LessonAllocation.objects.filter(timetable_subject=subject,timetable_class=cls,timetable_term=term).count()
                                      if count <= num:
                                          cnt = LessonAllocation.objects.filter(timetable_day=day,timetable_subject=subject,timetable_class=cls,timetable_term=term).count()
                                          dbs = alloc.double_lessons
                                          doublecount = 0
                                          doublestracker = DoublesTracker()
                                          try:
                                              doublestracker = DoublesTracker.objects.get(
                                                  doubletracker_subject=subject,doubletracker_class=cls,doubletracker_term=term)
                                          except doublestracker.DoesNotExist:
                                              doublecount = 0

                                          else:
                                              doublecount = doublestracker.doubletracker_number

                                          if cnt == 0:
                                              tcount = 0
                                              teachersubject = TeacherSubjects()
                                              try:
                                                  teachersubject = TeacherSubjects.objects.get(teacher_subjectclass=cls,teacher_subjectsubject=subject)
                                                  teacher = Teachers.objects.get( pk=teachersubject.teacher_subjectteacher.pk)
                                              except teachersubject.DoesNotExist:
                                                  print('Teacher Does not Exist!')
                                                  break
                                              else:
                                                  tcount = LessonAllocation.objects.filter(timetable_day=day,timetable_lesson=lesson,timetable_teacher=teacher,
                                                                                           timetable_term=term).count()


                                                  if tcount == 0:

                                                      if alloc.stroked_subject:
                                                          stroked = alloc.stroked_with
                                                          strokedsubject = ClassSubjects.objects.filter(stroked_with=stroked, classsubject_class=cls)
                                                          if strokedsubject:
                                                              for stro in strokedsubject:
                                                                  subj = Subjects.objects.get(pk=stro.classsubject_subject.pk)
                                                                  classstrk = SchoolClasses.objects.get(pk=stro.classsubject_class.pk)
                                                                  teachersubject = TeacherSubjects()
                                                                  try:
                                                                      teachersubject = TeacherSubjects.objects.get(teacher_subjectclass=classstrk,teacher_subjectsubject=subj)
                                                                      subjs = Subjects.objects.get(pk=teachersubject.teacher_subjectsubject.pk)
                                                                  except teachersubject.DoesNotExist:
                                                                      delestroked = LessonAllocation.objects.filter(timetable_day=day,timetable_lesson=lesson,timetable_class=classstrk)
                                                                      if delestroked:
                                                                          for dele in delestroked:
                                                                              delesson = LessonAllocation.objects.get(pk=dele.timetable_code)
                                                                              delesson.delete()

                                                                              print(subj.subject_name + ' has no teacher assigned in ' + classstrk.class_name + ' and it is stroked with ' + subject.subject_name)
                                                                              #find another slots
                                                                              break

                                                                  else:
                                                                      strteacher = Teachers.objects.get(pk=teachersubject.teacher_subjectteacher.pk)
                                                                      strcount = LessonAllocation.objects.filter(timetable_day=day,timetable_lesson=lesson,timetable_subject=subjs,timetable_teacher=strteacher).count()
                                                                      if strcount == 0:
                                                                          checkdup = LessonAllocation.objects.filter(timetable_day=day,timetable_lesson=lesson,timetable_subject=subj).count()
                                                                          if checkdup == 0:
                                                                              strokedTable = LessonAllocation()
                                                                              strokedTable.timetable_lesson =lesson
                                                                              strokedTable.timetable_day = day
                                                                              strokedTable.timetable_subject = subj
                                                                              strokedTable.timetable_teacher = strteacher
                                                                              strokedTable.timetable_term = term
                                                                              strokedTable.timetable_class = classstrk
                                                                              strokedTable.save()
                                                                          else:

                                                                              print(subj.subject_name + ' has the teacher assigned in another class at this lesson and its stroked with ' + subject.subject_name)
                                                                              break


                                                      else:
                                                              tt = LessonAllocation()
                                                              tt.timetable_day = day
                                                              tt.timetable_lesson = lesson
                                                              tt.timetable_class = cls
                                                              tt.timetable_subject = subject
                                                              tt.timetable_term = term
                                                              tt.timetable_teacher = teacher
                                                              tt.save()




                                          elif count == 1 and dbs > 0:
                                              if doublecount < dbs:
                                                      tcount = LessonAllocation.objects.filter(timetable_day=day,timetable_lesson=lesson,timetable_teacher=teacher).count()
                                                      if tcount == 0:

                                                          allocated2 = LessonAllocation.objects.get( timetable_day=day,timetable_subject=subject,
                                                              timetable_class=cls)

                                                          less1 = LessonSetups.objects.get(pk=allocated2.timetable_lesson.pk)
                                                          if less1.lesson_end == lesson.lesson_start:
                                                              if alloc.stroked_subject:
                                                                  stroked = alloc.stroked_with
                                                                  strokedsubject = ClassSubjects.objects.filter(stroked_with=stroked, classsubject_class=cls)
                                                                  if strokedsubject:
                                                                      for stro in strokedsubject:
                                                                          subj = Subjects.objects.get(pk=stro.classsubject_subject.pk)
                                                                          classstrk = SchoolClasses.objects.get(pk=stro.classsubject_class.pk)
                                                                          teachersubject = TeacherSubjects()
                                                                          try:
                                                                              teachersubject = TeacherSubjects.objects.get(teacher_subjectclass=classstrk,teacher_subjectsubject=subj)
                                                                              subjs = Subjects.objects.get(pk=teachersubject.teacher_subjectsubject.pk)

                                                                          except teachersubject.DoesNotExist:
                                                                              delestroked = LessonAllocation.objects.filter(timetable_day=day,timetable_lesson=lesson,timetable_class=classstrk)
                                                                              if delestroked:
                                                                                  for dele in delestroked:
                                                                                      delesson = LessonAllocation.objects.get( pk=dele.timetable_code)
                                                                                      delesson.delete()

                                                                                      print(subj.subject_name + ' has no teacher assigned in ' + classstrk.class_name + ' and it is stroked with' + subject.subject_name)
                                                                                      break

                                                                          else:
                                                                              strteacher = Teachers.objects.get(pk=teachersubject.teacher_subjectteacher.pk)
                                                                              strcount = LessonAllocation.objects.filter(timetable_day=day,timetable_lesson=lesson,timetable_subject=subjs,
                                                                                  timetable_teacher=strteacher).count()
                                                                              if strcount == 0:

                                                                                checkdup = LessonAllocation.objects.filter( timetable_day=day,timetable_lesson=lesson,timetable_subject=subj).count()
                                                                                if checkdup == 0:
                                                                                  strokedTable = LessonAllocation()
                                                                                  strokedTable.timetable_lesson = lesson
                                                                                  strokedTable.timetable_day =day
                                                                                  strokedTable.timetable_subject = subj
                                                                                  strokedTable.timetable_teacher = strteacher
                                                                                  strokedTable.timetable_term = term
                                                                                  strokedTable.timetable_class = classstrk
                                                                                  strokedTable.save()
                                                                                  doublestracker = DoublesTracker()
                                                                                  try:
                                                                                      doublestracker = DoublesTracker.objects.get(
                                                                                          doubletracker_subject=subject,
                                                                                          doubletracker_class=cls,
                                                                                          doubletracker_term=term)
                                                                                  except doublestracker.DoesNotExist:
                                                                                      dbtr = DoublesTracker()
                                                                                      dbtr.doubletracker_number = 0
                                                                                      dbtr.doubletracker_class = cls
                                                                                      dbtr.doubletracker_term = term
                                                                                      dbtr.doubletracker_subject = subject
                                                                                      dbtr.save()

                                                                                  else:
                                                                                      doublestracker.doubletracker_number = doublestracker.doubletracker_number + 1
                                                                                      doublestracker.save()

                                                                              else:

                                                                                 print(subj.subject_name + ' has the teacher assigned in another class at this lesson and its stroked with ' + subject.subject_name)
                                                                                 break
                                                                  else:
                                                                      tt = LessonAllocation()
                                                                      tt.timetable_day = day
                                                                      tt.timetable_lesson = lesson
                                                                      tt.timetable_class = cls
                                                                      tt.timetable_subject = subject
                                                                      tt.timetable_term = term
                                                                      tt.timetable_teacher = teacher
                                                                      tt.save()
                                                                      doublestracker = DoublesTracker()
                                                                      try:
                                                                          doublestracker = DoublesTracker.objects.get(
                                                                              doubletracker_subject=subject,
                                                                              doubletracker_class=cls,
                                                                              doubletracker_term=term)
                                                                      except doublestracker.DoesNotExist:
                                                                          dbtr = DoublesTracker()
                                                                          dbtr.doubletracker_number = 0
                                                                          dbtr.doubletracker_class = cls
                                                                          dbtr.doubletracker_term = term
                                                                          dbtr.doubletracker_subject = subject
                                                                          dbtr.save()

                                                                      else:
                                                                          doublestracker.doubletracker_number = doublestracker.doubletracker_number + 1
                                                                          doublestracker.save()

                                                              else:
                                                                  tt = LessonAllocation()
                                                                  tt.timetable_day = day
                                                                  tt.timetable_lesson = lesson
                                                                  tt.timetable_class = cls
                                                                  tt.timetable_subject = subject
                                                                  tt.timetable_term = term
                                                                  tt.timetable_teacher = teacher
                                                                  tt.save()
                                                                  doublestracker = DoublesTracker()
                                                                  try:
                                                                     doublestracker = DoublesTracker.objects.get(doubletracker_subject=subject,
                                                                                                                 doubletracker_class=cls,
                                                                                                                 doubletracker_term=term)
                                                                  except doublestracker.DoesNotExist:
                                                                      dbtr = DoublesTracker()
                                                                      dbtr.doubletracker_number = 0
                                                                      dbtr.doubletracker_class = cls
                                                                      dbtr.doubletracker_term = term
                                                                      dbtr.doubletracker_subject = subject
                                                                      dbtr.save()

                                                                  else:
                                                                      doublestracker.doubletracker_number = doublestracker.doubletracker_number + 1
                                                                      doublestracker.save()
                                                          else:
                                                              print('Double lessons should not have a break or a lesson between them')
                                                              break
                                                      else:
                                                         print(teacher.teacher_name+' is already assigned to another lesson in another class')
                                                         break

                                          elif count > 1:
                                                      print(subject.subject_name+' lesson already has a double today so its not possible to have it again')
                                                      break
                                      else:
                                          print('Subject '+subject.subject_name+' has had maximum number of lessons per week')
                                          break
                                    else:
                                        print('Lesson '+lesson.lesson_name+' already has a subject assigned to it!')
                            else:
                                print('Lessons need to be setup for timetable processing!')
                    else:
                        print('Class Subjects need to be setup for timetable processing!')
            else:
                print('Classes require to be setup for timetable processing')
    else:
        print('Days require to be setup for timetable processing')

    return JsonResponse({'success': 'Generated Successfully'})


# def generatetimetable(request):
#
#     term = TermDates.objects.get(current_term=True)
#     days = DaySetups.objects.all()
#     if days:
#            for day in days:
#                lessons = LessonSetups.objects.raw("select * from lessonsetups_lessonsetups" +
#                                                   " order by lesson_start")
#                if lessons:
#                    for lesson in lessons:
#                        classes = SchoolClasses.objects.all()
#                        if classes:
#                            for cls in classes:
#                              allocs = ClassSubjects.objects.raw("select * from classsubjects_classsubjects" +
#                                                                   " inner join subjects_subjects ss on classsubjects_classsubjects.classsubject_subject_id = ss.subject_code" +
#                                                                   " inner join classes_schoolclasses cs on classsubjects_classsubjects.classsubject_class_id = cs.class_code" +
#                                                                   " order by class_name,cast(subject_order as numeric)")
#                              if allocs:
#                                subject = Subjects.objects.get(pk=alloc.classsubject_subject.pk)
#                                allocclass = SchoolClasses.objects.get(pk=alloc.classsubject_class.pk)
#                                ttcount = LessonAllocation.objects.filter(timetable_lesson=lesson,
#                                                 timetable_class=allocclass,
#                                                 timetable_term=term,
#                                                 timetable_day=day).count()
#                                if ttcount == 0:
#                                    num = alloc.lessons_perweek
#                                    count = LessonAllocation.objects.filter(
#                                        timetable_subject=subject,
#                                        timetable_class=allocclass,
#                                        timetable_term=term).count()
#                                    if count<=num:
#                                        doubles = alloc.double_lessons
#                                        dcount = 0
#                                        ds = DoublesTracker.objects.filter(doubletracker_subject=subject,
#                                                                          doubletracker_class=allocclass,
#                                                                           doubletracker_term=term)
#
#                                        if ds:
#                                        for d in ds:
#                                            dcount = d.doubletracker_number
#                                            if dcount <= doubles:
#
#
#
#                                        else:
#
#
#
#                                        allocs = LessonAllocation.objects.get(timetable_day=timetabling.timetable_day,
#                                                                              timetable_subject=timetabling.timetable_subject,
#                                                                              timetable_class=timetabling.timetable_class)
#                              else:
#                                  return JsonResponse(
#                                      {
#                                          'error': 'No Subjects are Assigned to classes and they are required for timetable generation'},
#                                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#
#
#
#                        else:
#                            return JsonResponse(
#                                {
#                                    'error': 'No Subjects are Assigned to classes and they are required for timetable generation'},
#                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#                else:
#                     return JsonResponse(
#                         {'error': 'Lessons are required for timetable generation!'},
#                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             return JsonResponse(
#                 {'error': 'Days are required to be setup for timetable generation'},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # if td is not None and td != '':
    #     day = DaySetups.objects.get(pk=td)
    #     timetabling.timetable_day = day
    #
    # if tc is not None and tc != '':
    #     classes = SchoolClasses.objects.get(pk=tc)
    #     timetabling.timetable_class = classes
    #
    # if tl is not None and tl != '':
    #     lesson = LessonSetups.objects.get(pk=tl)
    #     timetabling.timetable_lesson = lesson
    #
    # if tt is not None and tt != '':
    #     term = TermDates.objects.get(pk=tt)
    #     timetabling.timetable_term = term
    #
    # if ts is not None and ts != '':
    #     subject = Subjects.objects.get(pk=ts)
    #     timetabling.timetable_subject = subject
    #
    # if tts is not None and tts != '':
    #     teacher = Teachers.objects.get(pk=tts)
    #     timetabling.timetable_teacher = teacher
def get_timetableData(code):
    tt = LessonAllocation.objects.raw("select timetable_code,timetable_name,day_name,subject_name,lesson_start,lesson_end,teacher_name,subject_code,day_code from lessonallocation_lessonallocation"+
                                       " inner join subjects_subjects ss on lessonallocation_lessonallocation.timetable_subject_id = ss.subject_code"+
                                       " inner join teachers_teachers tt on lessonallocation_lessonallocation.timetable_teacher_id = tt.teacher_code"+
                                       " inner join classes_schoolclasses cs on lessonallocation_lessonallocation.timetable_class_id = cs.class_code"+
                                       " inner join termdates_termdates t on lessonallocation_lessonallocation.timetable_term_id = t.term_code"+
                                       " inner join lessonsetups_lessonsetups ll on lessonallocation_lessonallocation.timetable_lesson_id = ll.lesson_code"+
                                       " inner join daysetups_daysetups dd on lessonallocation_lessonallocation.timetable_day_id = dd.day_code"+
                                       " where class_code = %s"+
                                       " order by day_code,day_name,subject_code,subject_name,lesson_start,lesson_end,teacher_name,timetable_code",[code])
    listsel = []

    for obj in tt:
        if obj.timetable_code not in listsel:
            response_data = {}
            start = obj.lesson_start.strftime('%H:%M')
            end = obj.lesson_end.strftime('%H:%M')
            com = start + '-' + end
            response_data['Day'] = obj.day_name
            response_data[com] = obj.timetable_name





            listsel.append(response_data)

    # for obj in tt:
    #     if obj.timetable_code not in listsel:
    #         response_data = {}
    #         start = obj.lesson_start.strftime('%H:%M')
    #         end = obj.lesson_end.strftime('%H:%M')
    #         com = start + '-' + end
    #         response_data['Day'] = obj.day_name
    #         response_data[com] = obj.timetable_name
    #
    #
    #
    #
    #
    #         listsel.append(response_data)

    # df = pd.DataFrame(listsel, columns=['Code','FatherName', 'FatherAddress','FatherPhone','FatherEmail','IDNO','FatherProffession','ParentOrGuardian',
    #                                'EmailRequired','MotherName','MotherAddress','MotherPhone','MotherEmail','MotherProffession'])

    df = pd.DataFrame(listsel)
    print(df)
    return df

def get_timetableData2(code,term):
    listsel = []
    days = DaySetups.objects.all()



    for day in days:
        response_data = {}
        tt = LessonAllocation.objects.raw(
                  "select timetable_code,day_name,class_name,timetable_name,subject_name,lesson_start,lesson_end,teacher_name,subject_code,day_code from lessonallocation_lessonallocation" +
                  " inner join subjects_subjects ss on lessonallocation_lessonallocation.timetable_subject_id = ss.subject_code" +
                  " inner join teachers_teachers tt on lessonallocation_lessonallocation.timetable_teacher_id = tt.teacher_code" +
                  " inner join classes_schoolclasses cs on lessonallocation_lessonallocation.timetable_class_id = cs.class_code" +
                  " inner join termdates_termdates t on lessonallocation_lessonallocation.timetable_term_id = t.term_code" +
                  " inner join lessonsetups_lessonsetups ll on lessonallocation_lessonallocation.timetable_lesson_id = ll.lesson_code" +
                  " inner join daysetups_daysetups dd on lessonallocation_lessonallocation.timetable_day_id = dd.day_code" +
                  " where day_code= %s and class_code= %s and term_code= %s",
                  tuple([day.day_code, code, term]))
        for obj in tt:
          classsubject = ClassSubjects.objects.get(classsubject_subject=obj.subject_code, classsubject_class=code)
          strokes=''
          if classsubject.stroked_subject:
              stroked = classsubject.stroked_with
              strokedsubject = ClassSubjects.objects.filter(stroked_with=stroked, classsubject_class=code)
              if strokedsubject:
                  for stro in strokedsubject:
                      subj = Subjects.objects.get(pk=stro.classsubject_subject.pk)
                      if strokes=='':
                         strokes=strokes+subj.timetable_name
                      else:
                          strokes = strokes+'/' +subj.timetable_name



          start = obj.lesson_start.strftime('%H:%M')
          end = obj.lesson_end.strftime('%H:%M')
          com = start + '-' + end
          response_data['Day'] = obj.day_name
          response_data['Class'] = obj.class_name

          if strokes != '':
              response_data[com] = strokes
          else:
              response_data[com] = obj.timetable_name

        listsel.append(response_data)
    print(listsel)


    df = pd.DataFrame(listsel)
    print(df)
    return df


def generateExcel(request):
    if request.method == 'GET' and 'class_code' in request.GET:
        code = request.GET['class_code']
        term = request.GET['term_code']
        with BytesIO() as b:

          data = get_timetableData2(code,term)
          with pd.ExcelWriter(b) as writer:
               data.to_excel(writer, sheet_name='Timetable', index=False)

          filename = f"timetable.xlsx"
          res = HttpResponse(
                 b.getvalue(),
                 content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                 )
          res['Content-Disposition'] = f'attachment; filename={filename}'
          return res


def automatictimetablev1(request):
    days = DaySetups.objects.all()
    term = TermDates.objects.get(current_term=True)
    DoublesTracker.objects.filter(doubletracker_term=term).delete()
    LessonAllocation.objects.filter(timetable_term=term).delete()
    if days:
        for day in days:
            classes = SchoolClasses.objects.filter(active=True)
            if classes:
                for cls in classes:
                    allocs = ClassSubjects.objects.raw("select * from classsubjects_classsubjects" +
                                                       " inner join subjects_subjects ss on classsubjects_classsubjects.classsubject_subject_id = ss.subject_code" +
                                                       " inner join classes_schoolclasses cs on classsubjects_classsubjects.classsubject_class_id = cs.class_code" +
                                                       " where classsubject_class_id=%s"
                                                       " order by class_name,cast(subject_order as numeric)",
                                                       [cls.class_code])

                    if allocs:
                        for alloc in allocs:
                            print(alloc.subject_name)
                            lessons = LessonSetups.objects.raw("select * from lessonsetups_lessonsetups"
                                                               " where lesson_type='L'" +
                                                               " order by lesson_start")

                            if lessons:
                                for lesson in lessons:
                                    allocated = LessonAllocation.objects.filter(timetable_lesson=lesson,
                                                                                timetable_class=cls,
                                                                                timetable_term=term,
                                                                                timetable_day=day).count()
                                    if allocated == 0:
                                        num = alloc.lessons_perweek
                                        subject = Subjects.objects.get(pk=alloc.classsubject_subject.pk)
                                        count = LessonAllocation.objects.filter(timetable_subject=subject,
                                                                                timetable_class=cls,
                                                                                timetable_term=term).count()
                                        if count <= num:
                                            cnt = LessonAllocation.objects.filter(timetable_day=day,
                                                                                  timetable_subject=subject,
                                                                                  timetable_class=cls,
                                                                                  timetable_term=term).count()
                                            dbs = alloc.double_lessons
                                            doublecount = 0
                                            doublestracker = DoublesTracker()
                                            try:
                                                doublestracker = DoublesTracker.objects.get(
                                                    doubletracker_subject=subject, doubletracker_class=cls,
                                                    doubletracker_term=term)
                                            except doublestracker.DoesNotExist:
                                                doublecount = 0

                                            else:
                                                doublecount = doublestracker.doubletracker_number

                                            if cnt == 0:
                                                tcount = 0
                                                teachersubject = TeacherSubjects()
                                                try:
                                                    teachersubject = TeacherSubjects.objects.get(
                                                        teacher_subjectclass=cls, teacher_subjectsubject=subject)
                                                    teacher = Teachers.objects.get(
                                                        pk=teachersubject.teacher_subjectteacher.pk)
                                                except teachersubject.DoesNotExist:
                                                    print('Teacher Does not Exist!')
                                                    break
                                                else:
                                                    tcount = LessonAllocation.objects.filter(timetable_day=day,
                                                                                             timetable_lesson=lesson,
                                                                                             timetable_teacher=teacher,
                                                                                             timetable_term=term).count()

                                                    if tcount == 0:

                                                        if alloc.stroked_subject:
                                                            stroked = alloc.stroked_with
                                                            strokedsubject = ClassSubjects.objects.filter(
                                                                stroked_with=stroked, classsubject_class=cls)
                                                            if strokedsubject:
                                                                for stro in strokedsubject:
                                                                    subj = Subjects.objects.get(
                                                                        pk=stro.classsubject_subject.pk)
                                                                    classstrk = SchoolClasses.objects.get(
                                                                        pk=stro.classsubject_class.pk)
                                                                    teachersubject = TeacherSubjects()
                                                                    try:
                                                                        teachersubject = TeacherSubjects.objects.get(
                                                                            teacher_subjectclass=classstrk,
                                                                            teacher_subjectsubject=subj)
                                                                        subjs = Subjects.objects.get(
                                                                            pk=teachersubject.teacher_subjectsubject.pk)
                                                                    except teachersubject.DoesNotExist:
                                                                        delestroked = LessonAllocation.objects.filter(
                                                                            timetable_day=day, timetable_lesson=lesson,
                                                                            timetable_class=classstrk)
                                                                        if delestroked:
                                                                            for dele in delestroked:
                                                                                delesson = LessonAllocation.objects.get(
                                                                                    pk=dele.timetable_code)
                                                                                delesson.delete()

                                                                                print(
                                                                                    subj.subject_name + ' has no teacher assigned in ' + classstrk.class_name + ' and it is stroked with ' + subject.subject_name)
                                                                                # find another slots
                                                                                break

                                                                    else:
                                                                        strteacher = Teachers.objects.get(
                                                                            pk=teachersubject.teacher_subjectteacher.pk)
                                                                        strcount = LessonAllocation.objects.filter(
                                                                            timetable_day=day, timetable_lesson=lesson,
                                                                            timetable_subject=subjs,
                                                                            timetable_teacher=strteacher).count()
                                                                        if strcount == 0:
                                                                            checkdup = LessonAllocation.objects.filter(
                                                                                timetable_day=day,
                                                                                timetable_lesson=lesson,
                                                                                timetable_subject=subj).count()
                                                                            if checkdup == 0:
                                                                                strokedTable = LessonAllocation()
                                                                                strokedTable.timetable_lesson = lesson
                                                                                strokedTable.timetable_day = day
                                                                                strokedTable.timetable_subject = subj
                                                                                strokedTable.timetable_teacher = strteacher
                                                                                strokedTable.timetable_term = term
                                                                                strokedTable.timetable_class = classstrk
                                                                                strokedTable.save()
                                                                            else:

                                                                                print(
                                                                                    subj.subject_name + ' has the teacher assigned in another class at this lesson and its stroked with ' + subject.subject_name)
                                                                                break


                                                        else:
                                                            tt = LessonAllocation()
                                                            tt.timetable_day = day
                                                            tt.timetable_lesson = lesson
                                                            tt.timetable_class = cls
                                                            tt.timetable_subject = subject
                                                            tt.timetable_term = term
                                                            tt.timetable_teacher = teacher
                                                            tt.save()




                                            elif count == 1 and dbs > 0:
                                                if doublecount < dbs:
                                                    tcount = LessonAllocation.objects.filter(timetable_day=day,
                                                                                             timetable_lesson=lesson,
                                                                                             timetable_teacher=teacher).count()
                                                    if tcount == 0:

                                                        allocated2 = LessonAllocation.objects.get(timetable_day=day,
                                                                                                  timetable_subject=subject,
                                                                                                  timetable_class=cls)

                                                        less1 = LessonSetups.objects.get(
                                                            pk=allocated2.timetable_lesson.pk)
                                                        if less1.lesson_end == lesson.lesson_start:
                                                            if alloc.stroked_subject:
                                                                stroked = alloc.stroked_with
                                                                strokedsubject = ClassSubjects.objects.filter(
                                                                    stroked_with=stroked, classsubject_class=cls)
                                                                if strokedsubject:
                                                                    for stro in strokedsubject:
                                                                        subj = Subjects.objects.get(
                                                                            pk=stro.classsubject_subject.pk)
                                                                        classstrk = SchoolClasses.objects.get(
                                                                            pk=stro.classsubject_class.pk)
                                                                        teachersubject = TeacherSubjects()
                                                                        try:
                                                                            teachersubject = TeacherSubjects.objects.get(
                                                                                teacher_subjectclass=classstrk,
                                                                                teacher_subjectsubject=subj)
                                                                            subjs = Subjects.objects.get(
                                                                                pk=teachersubject.teacher_subjectsubject.pk)

                                                                        except teachersubject.DoesNotExist:
                                                                            delestroked = LessonAllocation.objects.filter(
                                                                                timetable_day=day,
                                                                                timetable_lesson=lesson,
                                                                                timetable_class=classstrk)
                                                                            if delestroked:
                                                                                for dele in delestroked:
                                                                                    delesson = LessonAllocation.objects.get(
                                                                                        pk=dele.timetable_code)
                                                                                    delesson.delete()

                                                                                    print(
                                                                                        subj.subject_name + ' has no teacher assigned in ' + classstrk.class_name + ' and it is stroked with' + subject.subject_name)
                                                                                    break

                                                                        else:
                                                                            strteacher = Teachers.objects.get(
                                                                                pk=teachersubject.teacher_subjectteacher.pk)
                                                                            strcount = LessonAllocation.objects.filter(
                                                                                timetable_day=day,
                                                                                timetable_lesson=lesson,
                                                                                timetable_subject=subjs,
                                                                                timetable_teacher=strteacher).count()
                                                                            if strcount == 0:

                                                                                checkdup = LessonAllocation.objects.filter(
                                                                                    timetable_day=day,
                                                                                    timetable_lesson=lesson,
                                                                                    timetable_subject=subj).count()
                                                                                if checkdup == 0:
                                                                                    strokedTable = LessonAllocation()
                                                                                    strokedTable.timetable_lesson = lesson
                                                                                    strokedTable.timetable_day = day
                                                                                    strokedTable.timetable_subject = subj
                                                                                    strokedTable.timetable_teacher = strteacher
                                                                                    strokedTable.timetable_term = term
                                                                                    strokedTable.timetable_class = classstrk
                                                                                    strokedTable.save()
                                                                                    doublestracker = DoublesTracker()
                                                                                    try:
                                                                                        doublestracker = DoublesTracker.objects.get(
                                                                                            doubletracker_subject=subject,
                                                                                            doubletracker_class=cls,
                                                                                            doubletracker_term=term)
                                                                                    except doublestracker.DoesNotExist:
                                                                                        dbtr = DoublesTracker()
                                                                                        dbtr.doubletracker_number = 0
                                                                                        dbtr.doubletracker_class = cls
                                                                                        dbtr.doubletracker_term = term
                                                                                        dbtr.doubletracker_subject = subject
                                                                                        dbtr.save()

                                                                                    else:
                                                                                        doublestracker.doubletracker_number = doublestracker.doubletracker_number + 1
                                                                                        doublestracker.save()

                                                                            else:

                                                                                print(
                                                                                    subj.subject_name + ' has the teacher assigned in another class at this lesson and its stroked with ' + subject.subject_name)
                                                                                break
                                                                else:
                                                                    tt = LessonAllocation()
                                                                    tt.timetable_day = day
                                                                    tt.timetable_lesson = lesson
                                                                    tt.timetable_class = cls
                                                                    tt.timetable_subject = subject
                                                                    tt.timetable_term = term
                                                                    tt.timetable_teacher = teacher
                                                                    tt.save()
                                                                    doublestracker = DoublesTracker()
                                                                    try:
                                                                        doublestracker = DoublesTracker.objects.get(
                                                                            doubletracker_subject=subject,
                                                                            doubletracker_class=cls,
                                                                            doubletracker_term=term)
                                                                    except doublestracker.DoesNotExist:
                                                                        dbtr = DoublesTracker()
                                                                        dbtr.doubletracker_number = 0
                                                                        dbtr.doubletracker_class = cls
                                                                        dbtr.doubletracker_term = term
                                                                        dbtr.doubletracker_subject = subject
                                                                        dbtr.save()

                                                                    else:
                                                                        doublestracker.doubletracker_number = doublestracker.doubletracker_number + 1
                                                                        doublestracker.save()

                                                            else:
                                                                tt = LessonAllocation()
                                                                tt.timetable_day = day
                                                                tt.timetable_lesson = lesson
                                                                tt.timetable_class = cls
                                                                tt.timetable_subject = subject
                                                                tt.timetable_term = term
                                                                tt.timetable_teacher = teacher
                                                                tt.save()
                                                                doublestracker = DoublesTracker()
                                                                try:
                                                                    doublestracker = DoublesTracker.objects.get(
                                                                        doubletracker_subject=subject,
                                                                        doubletracker_class=cls,
                                                                        doubletracker_term=term)
                                                                except doublestracker.DoesNotExist:
                                                                    dbtr = DoublesTracker()
                                                                    dbtr.doubletracker_number = 0
                                                                    dbtr.doubletracker_class = cls
                                                                    dbtr.doubletracker_term = term
                                                                    dbtr.doubletracker_subject = subject
                                                                    dbtr.save()

                                                                else:
                                                                    doublestracker.doubletracker_number = doublestracker.doubletracker_number + 1
                                                                    doublestracker.save()
                                                        else:
                                                            print(
                                                                'Double lessons should not have a break or a lesson between them')
                                                            break
                                                    else:
                                                        print(
                                                            teacher.teacher_name + ' is already assigned to another lesson in another class')
                                                        break

                                            elif count > 1:
                                                print(
                                                    subject.subject_name + ' lesson already has a double today so its not possible to have it again')
                                                break
                                        else:
                                            print(
                                                'Subject ' + subject.subject_name + ' has had maximum number of lessons per week')
                                            break
                                    else:
                                        print('Lesson ' + lesson.lesson_name + ' already has a subject assigned to it!')
                            else:
                                print('Lessons need to be setup for timetable processing!')
                    else:
                        print('Class Subjects need to be setup for timetable processing!')
            else:
                print('Classes require to be setup for timetable processing')
    else:
        print('Days require to be setup for timetable processing')

    return JsonResponse({'success': 'Generated Successfully'})


# def solveteacherallocated(cls,lesson,teacher):
    #query unallocated teachers and first one allocate there



