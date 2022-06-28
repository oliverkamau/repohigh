import json
from urllib.parse import urlsplit

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_control

from exams.processing.models import ExamProcessing
from exams.registration.models import ExamRegistration
from feemanager.managebalances.invoicedetails.models import BalanceTrackerDetails
from feemanager.managebalances.singleinvoicing.models import BalanceTracker
from feemanager.recievefees.models import FeePayment
from localities.forms import StudentForm, CountriesForm, CountiesForm
from localities.serializers import Select2Serializer
from setups.academics.classes.models import SchoolClasses
from setups.academics.gradingsystem.models import GradingSystem
from setups.academics.subjects.models import Subjects
from setups.academics.termdates.models import TermDates
from setups.academics.years.models import Years
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

def searchexamterm(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    terms = TermDates.objects.raw(
        "SELECT top 5 term_code,term_number FROM termdates_termdates WHERE term_number like %s order by term_number asc",
        [query])

    for obj in terms:
        select2 = Select2Data()
        select2.id = str(obj.term_code)
        select2.text = obj.term_number
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})

def searchexamyear(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    sources = Years.objects.raw(
        "SELECT top 5 year_code,year_number FROM years_years WHERE year_number like %s or year_name like %s",
        tuple([query, query]))

    for obj in sources:
        text = str(obj.year_number)
        select2 = Select2Data()
        select2.id = str(obj.year_code)
        select2.text = text
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

def searchexamregister(request,term,year):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    terms = ExamRegistration.objects.raw(
        "SELECT top 5 exam_reg_code,exam_name FROM registration_examregistration WHERE exam_term_id = %s and exam_year_id = %s and exam_name like %s",
        [term,year,query])

    for obj in terms:
        select2 = Select2Data()
        select2.id = str(obj.exam_reg_code)
        select2.text = obj.exam_name
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchsubjects(request,classcode):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    classes = Subjects.objects.raw(
        # "SELECT top 5 teacher_subjectcode,subject_name FROM teachersubjects_teachersubjects"+
        # " inner join subjects_subjects  on teacher_subjectsubject_id = subject_code"+
        # " WHERE teacher_subjectclass_id = %s and teacher_subjectteacher_id = %s and subject_name like %s",
        "SELECT top 5 subject_code,subject_name from subjects_subjects where subject_code in("+
        "SELECT teacher_subjectsubject_id FROM teachersubjects_teachersubjects where teacher_subjectclass_id=%s and subject_name like %s)",
        [classcode,query])

    for obj in classes:
        text = obj.subject_name
        select2 = Select2Data()
        select2.id = str(obj.subject_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})

def examchartdata(request):

    examCode = request.GET['examCode']
    classCode = request.GET['classCode']
    subjectCode = request.GET['subjectCode']
    reg = ExamRegistration.objects.get(pk=examCode)
    cls = SchoolClasses.objects.get(pk=classCode)
    subject = Subjects.objects.get(pk=subjectCode)

    grades = GradingSystem.objects.all()
    data = []
    labels = []
    perfomances = []
    colors = []
    background = []
    if grades:
        for grade in grades:
                labels.append(grade.grading_grade)

    if labels:
        for label in labels:
            count = ExamProcessing.objects.filter(exam_process_exam=reg,
                                        exam_process_subject=subject,
                                        exam_process_class=cls,
                                               exam_processing_grade=label).count()
            perfomances.append(count)



    x = len(perfomances)

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

    if x == 9:
        colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        colors.append('#9B59B6')
        colors.append('#26B99A')
        colors.append('#49A9EA')
        colors.append('#88B04B')
        colors.append('#FF6F61')
        colors.append('#E37383')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')
        background.append('#B370CF')
        background.append('#36CAAB')
        background.append('#b3d4ff')
        background.append('#F7CAC9')
        background.append('#F7CAC9')
        background.append('#FFF5EE')

    if x == 10:
        colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        colors.append('#9B59B6')
        colors.append('#26B99A')
        colors.append('#49A9EA')
        colors.append('#88B04B')
        colors.append('#FF6F61')
        colors.append('#E37383')
        colors.append('#FFF5EE')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')
        background.append('#B370CF')
        background.append('#36CAAB')
        background.append('#b3d4ff')
        background.append('#F7CAC9')
        background.append('#F7CAC9')
        background.append('#FFF5EE')
        background.append('#C21E56')

    if x == 11:
        colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        colors.append('#9B59B6')
        colors.append('#26B99A')
        colors.append('#49A9EA')
        colors.append('#88B04B')
        colors.append('#FF6F61')
        colors.append('#E37383')
        colors.append('#E0BFB8')
        colors.append('#673147')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')
        background.append('#B370CF')
        background.append('#36CAAB')
        background.append('#b3d4ff')
        background.append('#F7CAC9')
        background.append('#F7CAC9')
        background.append('#FFF5EE')
        background.append('#C21E56')
        background.append('#FF10F0')

    if x == 12:
        colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        colors.append('#9B59B6')
        colors.append('#26B99A')
        colors.append('#49A9EA')
        colors.append('#88B04B')
        colors.append('#FF6F61')
        colors.append('#E37383')
        colors.append('#E0BFB8')
        colors.append('#673147')
        colors.append('#D8BFD8')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')
        background.append('#B370CF')
        background.append('#36CAAB')
        background.append('#b3d4ff')
        background.append('#F7CAC9')
        background.append('#F7CAC9')
        background.append('#FFF5EE')
        background.append('#C21E56')
        background.append('#FF10F0')
        background.append('#26B99A')

    if x == 13:
        colors.append('#50e991')
        colors.append('#b3d4ff')
        colors.append('#3498DB')
        colors.append('#9B59B6')
        colors.append('#26B99A')
        colors.append('#49A9EA')
        colors.append('#88B04B')
        colors.append('#FF6F61')
        colors.append('#E37383')
        colors.append('#E0BFB8')
        colors.append('#673147')
        colors.append('#D8BFD8')
        colors.append('#F2D2BD')
        background.append('#34495E')
        background.append('#CFD4D8')
        background.append('#49A9EA')
        background.append('#B370CF')
        background.append('#36CAAB')
        background.append('#b3d4ff')
        background.append('#F7CAC9')
        background.append('#F7CAC9')
        background.append('#FFF5EE')
        background.append('#C21E56')
        background.append('#FF10F0')
        background.append('#26B99A')
        background.append('#DE3163')




    data.append(labels)
    data.append(perfomances)
    data.append(colors)
    data.append(background)

    return JsonResponse(data,safe=False)