import json
from urllib.parse import urlsplit

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_control

from feemanager.managebalances.invoicedetails.models import BalanceTrackerDetails
from feemanager.managebalances.singleinvoicing.models import BalanceTracker
from feemanager.recievefees.models import FeePayment
from localities.forms import StudentForm, CountriesForm, CountiesForm
from localities.serializers import Select2Serializer
from setups.academics.classes.models import SchoolClasses
from setups.accounts.paymentmodes.models import PaymentModes
from staff.teachers.models import Teachers
from studentmanager.student.models import Students
from .models import StudentDef, Select2Data, Countries, Counties


# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def home(request):
    return render(request,'home/home.html')

def genderdata(request):
    male = Students.objects.filter(Q(student_gender='M'),(Q(student_school_status='Active') | Q(student_school_status='Leave') | Q(student_school_status='Suspended'))).count()
    female = Students.objects.filter(Q(student_gender='F'),(Q(student_school_status='Active') | Q(student_school_status='Leave') | Q(student_school_status='Suspended'))).count()
    gender = []
    gender.append(male)
    gender.append(female)
    return JsonResponse(gender,safe=False)


def getstats(request):
    students = Students.objects.filter(Q(student_school_status='Active') | Q(student_school_status='Leave') | Q(student_school_status='Suspended')).count()
    teachers = Teachers.objects.filter(status='Active').count()
    inschool = Students.objects.filter(student_school_status='Active').count()
    outofSchool = Students.objects.filter(Q(student_school_status='Leave') | Q(student_school_status='Suspended')).count()
    response = {}
    response['total']=students
    response['teachers'] = teachers
    response['inschool'] = inschool
    response['outofschool'] = outofSchool
    return JsonResponse(response)

def classdata(request):

    classes = SchoolClasses.objects.filter(active=True)
    data = []
    forms = []
    labels = []
    students = []
    colors = []
    background = []
    if classes:
        for cls in classes:
            if int(cls.form) not in forms:
                forms.append(int(cls.form))
                labels.append('Form '+cls.form)

    if forms:
        for form in forms:
            count = Students.objects.filter(student_class__form=form).count()
            students.append(count)

    x = len(forms)

    if x == 1:
        colors.append('#50e991')
        background.append('#34495E')
    if x == 2:
        colors.append('#50e991')
        colors.append('#b3d4ff')
        background.append('#34495E')
        background.append('#CFD4D8')

    if x == 3:
        colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')

    if x == 4:
        colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        colors.append('#9B59B6')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')
        background.append('#B370CF')

    if x == 5:
        colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        colors.append('#9B59B6')
        colors.append('#26B99A')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')
        background.append('#B370CF')
        background.append('#36CAAB')


    if x == 6:
        colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        colors.append('#9B59B6')
        colors.append('#26B99A')
        colors.append('#49A9EA')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')
        background.append('#B370CF')
        background.append('#36CAAB')
        background.append('#b3d4ff')

    if x == 7:
        colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        colors.append('#9B59B6')
        colors.append('#26B99A')
        colors.append('#49A9EA')
        colors.append('#88B04B')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')
        background.append('#B370CF')
        background.append('#36CAAB')
        background.append('#b3d4ff')
        background.append('#F7CAC9')

    if x == 8:
        colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        colors.append('#9B59B6')
        colors.append('#26B99A')
        colors.append('#49A9EA')
        colors.append('#88B04B')
        colors.append('#FF6F61')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')
        background.append('#B370CF')
        background.append('#36CAAB')
        background.append('#b3d4ff')
        background.append('#F7CAC9')
        background.append('#F7CAC9')




    data.append(labels)
    data.append(students)
    data.append(colors)
    data.append(background)

    return JsonResponse(data,safe=False)


def paymentmodes(request):
    data = []
    modes = []
    labels = []
    fees = []
    colors = []
    background = []
    payments = PaymentModes.objects.all()
    if payments:
       for mode in payments:
           modes.append(mode.payment_code)
           labels.append(mode.payment_name)


    if modes:
        for mode in modes:
            balance = 0
            feepays = FeePayment.objects.filter(payment_mode=mode)
            if feepays:
                for pay in feepays:
                    balance = balance + pay.payment_amount


            fees.append(balance)




    x = len(modes)

    if x == 1:
        colors.append('#9B59B6')

        # colors.append('#50e991')
        background.append('#34495E')


    if x == 2:
        colors.append('#9B59B6')
        colors.append('#88B04B')
        # colors.append('#50e991')
        # colors.append('#b3d4ff')
        background.append('#34495E')
        background.append('#CFD4D8')

    if x == 3:
        colors.append('#9B59B6')
        colors.append('#88B04B')
        # colors.append('#50e991')
        colors.append('#b3d4ff')
        # colors.append('#3498DB')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')

    if x == 4:
        colors.append('#9B59B6')
        colors.append('#88B04B')
        # colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        # colors.append('#9B59B6')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')
        background.append('#B370CF')

    if x == 5:
        colors.append('#9B59B6')
        colors.append('#88B04B')
        # colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        colors.append('#9B59B6')
        colors.append('#26B99A')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')
        background.append('#B370CF')
        background.append('#36CAAB')


    if x == 6:
        colors.append('#9B59B6')
        colors.append('#88B04B')
        # colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        colors.append('#9B59B6')
        colors.append('#26B99A')
        # colors.append('#49A9EA')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')
        background.append('#B370CF')
        background.append('#36CAAB')
        background.append('#b3d4ff')

    if x == 7:
        colors.append('#9B59B6')
        colors.append('#88B04B')
        # colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        colors.append('#9B59B6')
        colors.append('#26B99A')
        colors.append('#49A9EA')
        # colors.append('#88B04B')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')
        background.append('#B370CF')
        background.append('#36CAAB')
        background.append('#b3d4ff')
        background.append('#F7CAC9')

    if x == 8:
        colors.append('#9B59B6')
        colors.append('#88B04B')
        # colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        colors.append('#9B59B6')
        colors.append('#26B99A')
        colors.append('#49A9EA')
        # colors.append('#88B04B')
        colors.append('#FF6F61')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')
        background.append('#B370CF')
        background.append('#36CAAB')
        background.append('#b3d4ff')
        background.append('#F7CAC9')
        background.append('#F7CAC9')




    data.append(labels)
    data.append(fees)
    data.append(colors)
    data.append(background)

    return JsonResponse(data,safe=False)


def feebalances(request):

    classes = SchoolClasses.objects.filter(active=True)
    data = []
    forms = []
    labels = []
    fees = []
    colors = []
    background = []
    if classes:
        for cls in classes:
            if int(cls.form) not in forms:
                forms.append(int(cls.form))
                labels.append('Form '+cls.form+' Balance')

    if forms:
        for form in forms:
            balance = 0

            students = Students.objects.filter(student_class__form=form)
            if students:
                for std in students:
                    print(std.student_code)
                    tempbal = 0
                    tracker = BalanceTracker()
                    try:
                        tracker = BalanceTracker.objects.get(tracker_student=std)
                    except tracker.DoesNotExist:
                         print('Student '+std.student_name+' '+std.adm_no+' has no balance tracker')
                    else:
                        tracker = BalanceTracker.objects.get(tracker_student=std)
                        details = BalanceTrackerDetails.objects.filter(trackerdetails_tracker=tracker)
                        for detail in details:
                            tempbal = tempbal + detail.trackerdetails_balance
                    balance = balance + tempbal

            fees.append(balance)




    x = len(forms)

    if x == 1:
        colors.append('#50e991')
        background.append('#34495E')
    if x == 2:
        colors.append('#50e991')
        colors.append('#b3d4ff')
        background.append('#34495E')
        background.append('#CFD4D8')

    if x == 3:
        colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')

    if x == 4:
        colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        colors.append('#9B59B6')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')
        background.append('#B370CF')

    if x == 5:
        colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        colors.append('#9B59B6')
        colors.append('#26B99A')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')
        background.append('#B370CF')
        background.append('#36CAAB')


    if x == 6:
        colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        colors.append('#9B59B6')
        colors.append('#26B99A')
        colors.append('#49A9EA')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')
        background.append('#B370CF')
        background.append('#36CAAB')
        background.append('#b3d4ff')

    if x == 7:
        colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        colors.append('#9B59B6')
        colors.append('#26B99A')
        colors.append('#49A9EA')
        colors.append('#88B04B')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')
        background.append('#B370CF')
        background.append('#36CAAB')
        background.append('#b3d4ff')
        background.append('#F7CAC9')

    if x == 8:
        colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        colors.append('#9B59B6')
        colors.append('#26B99A')
        colors.append('#49A9EA')
        colors.append('#88B04B')
        colors.append('#FF6F61')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')
        background.append('#B370CF')
        background.append('#36CAAB')
        background.append('#b3d4ff')
        background.append('#F7CAC9')
        background.append('#F7CAC9')




    data.append(labels)
    data.append(fees)
    data.append(colors)
    data.append(background)

    return JsonResponse(data,safe=False)
# def add(request):
#     # firstName = request.POST['firstName']
#     # lastName = request.POST['lastName']
#     # age = int(request.POST['age'])
#     # height = int(request.POST['height'])
#     # country = request.POST['country']
#     # county = request.POST['county']
#     # town = request.POST['town']
#     # phone = request.POST['phone']
#     # website = request.POST['website']
#     # student = StudentDef()
#     # student.age = age
#     # student.firstName = firstName
#     # student.lastName = lastName
#     # student.height = height
#     # student.country = country
#     # student.county = county
#     # student.town = town
#     # student.phone = phone
#     # student.website = website
#     # student.save()
#     student = StudentForm(request.POST, request.FILES)
#     image = request.FILES.get('photo')
#     student.photo = image
#     country = Countries.objects.get(pk=student.data['stud_country'])
#     county  = Counties.objects.get(pk=student.data['stud_county'])
#     student.stud_country=country
#     student.stud_county=county
#     student.save()
#     return JsonResponse({'success': 'Student Saved Successfully'})
#
# def getStudents(request):
#     # localities = json.loads(serializers.serialize('json', StudentDef.objects.all()))
#     # return JsonResponse(localities, safe=False)
#     listsel = []
#     students = StudentDef.objects.raw(
#         "SELECT stdCode,concat(firstName,' ',lastName)name,phone,website,age,town,country_name,county_name FROM students_studentdef" +
#         " INNER JOIN students_countries on stud_country_id=country_id"+
#         " INNER JOIN students_counties on stud_county_id=county_id")
#
#     for obj in students:
#         response_data = {}
#         response_data['stdCode'] = obj.stdCode
#         response_data['country_name'] = obj.country_name
#         response_data['county_name'] = obj.county_name
#         response_data['name'] = obj.name
#         response_data['town'] = obj.town
#         response_data['phone'] = obj.phone
#         response_data['website'] = obj.website
#         response_data['age'] = obj.age
#
#
#         listsel.append(response_data)
#
#     return JsonResponse(listsel, safe=False)
#
# def editStudent(request,id):
#     print('This is the Id: '+str(id))
#     student = StudentDef.objects.get(pk=id)
#     country=Countries.objects.get(pk=student.stud_country.pk)
#     county = Counties.objects.get(pk=student.stud_county.pk)
#     response_data = {}
#     response_data['stdCode'] = student.stdCode
#     response_data['country_name'] = country.country_name
#     response_data['country_id'] = country.country_id
#     response_data['county_name'] = county.county_name
#     response_data['county_id'] = country.country_id
#     response_data['firstName'] = student.firstName
#     response_data['lastName'] = student.lastName
#     response_data['town'] = student.town
#     response_data['phone'] = student.phone
#     response_data['website'] = student.website
#     response_data['age'] = student.age
#     response_data['height'] = student.height
#     url = request.get_host()+student.photo.url
#     print(urlsplit(request.build_absolute_uri(None)).scheme)
#     response_data['url'] = urlsplit(request.build_absolute_uri(None)).scheme+'://'+request.get_host()+student.photo.url
#     return JsonResponse(response_data)
#
# def updateStudent(request,id):
#
#     student = StudentDef.objects.get(pk=id)
#     form = StudentForm(request.POST,instance=student)
#     form.save()
#     return JsonResponse({'success': 'Student Updated Successfully'})
#
# def deleteStudent(request,id):
#
#     student = StudentDef.objects.get(pk=id)
#     student.delete()
#     return JsonResponse({'success': 'Student Deleted Successfully'})
#
#
# def searchStudents(request):
#     if request.method == 'GET' and 'query' in request.GET:
#         query=request.GET['query']
#         query='%'+query+'%'
#     else:
#         query = '%' + '' + '%'
#
#     listsel = []
#     students = StudentDef.objects.raw("SELECT top 5 stdCode,firstName,lastName FROM students_studentdef WHERE firstName like %s or lastName like %s",tuple([query,query]))
#
#     for obj in students:
#         text = obj.firstName + ' ' + obj.lastName
#         select2 = Select2Data()
#         select2.id = str(obj.stdCode)
#         select2.text = text
#         serializer = Select2Serializer(select2)
#
#         listsel.append(serializer.data)
#
#
#     return JsonResponse({'results':listsel})
#
#
# def country(request):
#     return render(request,'countries.html')
#
#
# def addcountry(request):
#     country = CountriesForm(request.POST)
#     country.save()
#     return JsonResponse({'success': 'Country Saved Successfully'})
#
# def getcountry(request):
#     countries = json.loads(serializers.serialize('json', Countries.objects.all()))
#     return JsonResponse(countries, safe=False)
#
# def addcounty(request):
#     county = CountiesForm(request.POST)
#     print("Name: "+county.data['county_name']+"Code: "+county.data['county_code']+"Country: "+county.data['county_country'])
#     country= Countries.objects.get(pk=county.data['county_country'])
#     county.county_country = country
#     county.save()
#
#
#     return JsonResponse({'success': 'County Saved Successfully'})
#
#
# def getcounty(request):
#     # counties = json.loads(serializers.serialize('json', Counties.objects.all()))
#     # return JsonResponse(counties, safe=False)
#     listsel = []
#     counties = Counties.objects.raw(
#         "SELECT top 5 county_id,county_name,county_code,country_name FROM localities_counties"+
#         " INNER JOIN localities_counties on county_country_id=country_id")
#
#     for obj in counties:
#         response_data = {}
#         response_data['county_id'] = obj.county_id
#         response_data['county_name'] = obj.county_name
#         response_data['county_code'] = obj.county_code
#         response_data['country_name'] = obj.country_name
#
#         listsel.append(response_data)
#
#     return JsonResponse(listsel,safe=False)
#
# def searchcountries(request):
#     if request.method == 'GET' and 'query' in request.GET:
#         query = request.GET['query']
#         query = '%' + query + '%'
#     else:
#         query = '%' + '' + '%'
#
#     listsel = []
#     students = Countries.objects.raw(
#         "SELECT top 5 country_id,country_name FROM localities_counties WHERE country_name like %s or country_code like %s",
#         tuple([query, query]))
#
#     for obj in students:
#         text = obj.country_name
#         select2 = Select2Data()
#         select2.id = str(obj.country_id)
#         select2.text = text
#         serializer = Select2Serializer(select2)
#
#         listsel.append(serializer.data)
#
#     return JsonResponse({'results': listsel})
#
#
# def county(request):
#     return render(request,'counties.html')
#
#
# def searchcounties(request,id):
#     print('Id for search is :'+str(id))
#     if request.method == 'GET' and 'query' in request.GET:
#         query = request.GET['query']
#         query = '%' + query + '%'
#     else:
#         query = '%' + '' + '%'
#
#     listsel = []
#     counties = Counties.objects.raw(
#         "SELECT top 5 county_id,county_name FROM students_counties WHERE county_country_id = %s and" +
#         " (county_name like %s or county_code like %s)",
#         [id, query,query])
#
#     for obj in counties:
#         text = obj.county_name
#         select2 = Select2Data()
#         select2.id = str(obj.county_id)
#         select2.text = text
#         serializer = Select2Serializer(select2)
#
#         listsel.append(serializer.data)
#
#     return JsonResponse({'results': listsel})
#
#

