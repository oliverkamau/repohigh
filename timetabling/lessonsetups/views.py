from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_control
from rest_framework import status

from timetabling.lessonsetups.forms import LessonForm
from timetabling.lessonsetups.models import LessonSetups


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def lessonsetup(request):
    return render(request, 'timetabling/lessonsetups.html')


def createlesson(request):
    auto = ''
    if request.method == 'POST' and 'auto' in request.POST:
        val = request.POST['auto']
        auto = val
    else:
        auto = ''

    lesson = LessonForm(request.POST)
    setups = LessonSetups()
    start = lesson.data['lesson_start']
    end = lesson.data['lesson_end']
    duration = lesson.data['lesson_duration']
    name = lesson.data['lesson_name']
    type = lesson.data['lesson_type']
    setups.lesson_start = datetime.strptime(start, '%H:%M:%S')
    setups.lesson_name = name
    setups.lesson_end = datetime.strptime(end, '%H:%M:%S')
    setups.lesson_duration = duration
    setups.lesson_type = type
    if auto is not None and auto == 'on':
        setups.lesson_auto = True
    else:
        setups.lesson_auto = False
    lessname = LessonSetups.objects.filter(lesson_name=setups.lesson_name).count()
    if lessname > 0:
        return JsonResponse({'error': name+' is already defined!'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    lesson_sets = LessonSetups.objects.filter(lesson_start__range=(setups.lesson_start,setups.lesson_end))
    if not lesson_sets:
        setups.save()
    else:
        return JsonResponse({'error': 'Time range '+start+' to '+end+' already has a lesson'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse({'success': 'Lesson Saved Successfully!'})


def getlessons(request):
    listsel = []
    lessons = LessonSetups.objects.raw(
        "SELECT DISTINCT lesson_code,lesson_name,lesson_start,lesson_end,lesson_auto FROM lessonsetups_lessonsetups" +
        " order by lesson_code asc")

    for obj in lessons:
        if obj.lesson_code not in listsel:
            response_data = {}
            response_data['lesson_code'] = obj.lesson_code
            response_data['lesson_name'] = obj.lesson_name
            response_data['lesson_start'] = obj.lesson_start.strftime('%H:%M:%S')
            response_data['lesson_end'] = obj.lesson_end.strftime('%H:%M:%S')
            response_data['lesson_auto'] = obj.lesson_auto

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)

def editlesson(request,id):
    lesson = LessonSetups.objects.get(pk=id)
    response_data = {}

    response_data['lesson_code'] = lesson.lesson_code
    response_data['lesson_name'] = lesson.lesson_name
    response_data['lesson_start'] = lesson.lesson_start
    response_data['lesson_end'] = lesson.lesson_end
    response_data['lesson_auto'] = lesson.lesson_auto
    response_data['lesson_type'] = lesson.lesson_type
    response_data['lesson_duration'] = lesson.lesson_duration

    return JsonResponse(response_data)


def deletelesson(request,id):
    lesson = LessonSetups.objects.get(pk=id)
    lesson.delete()
    return JsonResponse({'success': 'Lesson Deleted Successfully'})


def updatelesson(request,id):
    lesson = LessonSetups.objects.get(pk=id)
    form = LessonForm(request.POST, instance=lesson)
    form.save()
    return JsonResponse({'success': 'Lesson Updated Successfully'})