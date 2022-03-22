from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_control

from timetabling.daysetups.forms import DayForm
from timetabling.daysetups.models import DaySetups


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def daysetups(request):
    return render(request, 'timetabling/daysetups.html')

def createday(request):
    days = DayForm(request.POST)
    days.save()
    return JsonResponse({'success': 'Day Saved Successfully'})

def getdays(request):
    listsel = []
    days = DaySetups.objects.raw(
        "SELECT DISTINCT day_code,day_name FROM daysetups_daysetups")


    for obj in days:
        if obj.day_code not in days:
           response_data = {}
           response_data['day_code'] = obj.day_code
           response_data['day_name'] = obj.day_name


           listsel.append(response_data)
    return JsonResponse(listsel, safe=False)


def editday(request,id):
    day = DaySetups.objects.get(pk=id)
    response_data = {}
    response_data['day_code'] = day.day_code
    response_data['day_name'] = day.day_name
    return JsonResponse(response_data)


def updateday(request,id):
    day = DaySetups.objects.get(pk=id)
    form = DayForm(request.POST, instance=day)
    form.save()
    return JsonResponse({'success': 'Day Updated Successfully'})


def deleteday(request,id):
    day = DaySetups.objects.get(pk=id)
    day.delete()
    return JsonResponse({'success': 'Day Deleted Successfully'})