import decimal

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status

from feemanager.pocketmoney.models import PocketMoneyTrans
from feemanager.pocketmoneytracker.models import PocketMoneyTracker
from localities.models import Select2Data
from localities.serializers import Select2Serializer
from setups.academics.classes.models import SchoolClasses
from setups.system.systemsequences.models import SystemSequences
from studentmanager.student.models import Students
from useradmin.users.models import User


def pocketmoneypage(request):
    return render(request, 'fees/pocketmoney.html')


def searchclass(request):
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

def searchstudents(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    students = Students.objects.raw(
        "SELECT top 5 student_code,adm_no,student_name from student_students where " +
        " adm_no like %s or student_name like %s",
        [query, query])

    for obj in students:
        text = obj.student_name + '-' + obj.adm_no
        select2 = Select2Data()
        select2.id = str(obj.student_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def savepocketmoney(request):

    stud = request.POST.get('student', None)
    trans = request.POST.get('transType', None)
    amount = request.POST.get('amount', None)
    date = request.POST.get('date', None)

    student = Students.objects.get(pk=stud)

    pockettracker = PocketMoneyTracker()
    try:
        pockettracker = PocketMoneyTracker.objects.get(tracker_student=student)

    except pockettracker.DoesNotExist:
        if trans == 'Deposit':
          tracker = PocketMoneyTracker()
          tracker.tracker_student = student
          tracker.tracker_date = date
          tracker.tracker_balance = decimal.Decimal(float(amount))
          tracker.save()
          if SystemSequences.objects.filter(sequence_type='Invoice').exists():
            seq = SystemSequences.objects.get(sequence_type='Invoice')
            tracker.tracker_invoiceno = 'INV00' + str(seq.sequence_nextseq)
            seq.sequence_nextseq = seq.sequence_nextseq + 1
            seq.save()
            tracker.save()
          else:
            seq = SystemSequences()
            seq.sequence_nextseq = 1
            seq.sequence_type = 'Invoice'
            seq.save()
            tracker.tracker_invoiceno = 'INV00' + str(seq.sequence_nextseq)
            tracker.save()
            seq.sequence_nextseq = seq.sequence_nextseq + 1
            seq.save()
        else:
            return JsonResponse({
                'error': 'You cannot withdraw from an empty account'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        pockettracker.tracker_date=date
        if trans=='Deposit':
           pockettracker.tracker_balance = decimal.Decimal(float(amount))+pockettracker.tracker_balance

        elif trans == 'Withdraw':
            if decimal.Decimal(float(amount)) > pockettracker.tracker_balance:
                return JsonResponse({
                    'error': 'Insufficient funds for withdrawal'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
              pockettracker.tracker_balance = pockettracker.tracker_balance - decimal.Decimal(float(amount))


        if SystemSequences.objects.filter(sequence_type='Invoice').exists():
            seq = SystemSequences.objects.get(sequence_type='Invoice')
            pockettracker.tracker_invoiceno = 'INV00' + str(seq.sequence_nextseq)
            seq.sequence_nextseq = seq.sequence_nextseq + 1
            seq.save()
            pockettracker.save()
        else:
            seq = SystemSequences()
            seq.sequence_nextseq = 1
            seq.sequence_type = 'Invoice'
            seq.save()
            pockettracker.tracker_invoiceno = 'INV00' + str(seq.sequence_nextseq)
            pockettracker.save()
            seq.sequence_nextseq = seq.sequence_nextseq + 1
            seq.save()

        pockettrans = PocketMoneyTrans()
        u = User.objects.get(username=request.user)
        pockettrans.pocketmoney_addedby = u
        pockettrans.pocketmoney_amount = decimal.Decimal(float(amount))
        pockettrans.pocketmoney_date = date
        pockettrans.pocketmoney_transtype = trans
        pockettrans.pocketmoney_student = student
        pockettrans.save()

    return JsonResponse({'success': 'Record Updated Successfully'})


def getbalance(request,id):
    pockettracker = PocketMoneyTracker()
    student = Students.objects.get(pk=id)
    response_data = {}
    try:
        pockettracker = PocketMoneyTracker.objects.get(tracker_student=student)

    except pockettracker.DoesNotExist:
        response_data['balance']=0.00

    else:
        response_data['balance']=pockettracker.tracker_balance

    return JsonResponse(response_data)


def getstudents(request):
    listsel = []
    students = Students.objects.raw(
        "SELECT student_code,adm_no,student_name,class_name,dorm_name,tracker_balance FROM pocketmoneytracker_pocketmoneytracker" +
        " left join student_students  on student_code = tracker_student_id" +
        " left join classes_schoolclasses ON student_class_id=class_code" +
        " left join dorms_dorms  on dorm_code = student_dorm_id" +
        " where student_school_status='Active'"
        " order by student_code desc"

    )
    for obj in students:
        if obj.student_code not in listsel:
            response_data = {}

            response_data['studentCode'] = obj.student_code
            response_data['name'] = obj.student_name
            response_data['admNo'] = obj.adm_no
            response_data['dorm'] = obj.dorm_name
            response_data['studentClass'] = obj.class_name
            response_data['balance'] = obj.tracker_balance

            listsel.append(response_data)

    return JsonResponse(listsel,safe=False)


def getstudentgrid(request,id):
    student = Students.objects.get(pk=id)
    response_data = {}
    response_data['studentName'] = student.student_name + '-' + student.adm_no
    response_data['studentCode'] = student.student_code
    pockettracker = PocketMoneyTracker()
    try:
        pockettracker = PocketMoneyTracker.objects.get(tracker_student=student)

    except pockettracker.DoesNotExist:
        response_data['balance'] = 0.00

    else:
        response_data['balance'] = pockettracker.tracker_balance

    return JsonResponse(response_data)