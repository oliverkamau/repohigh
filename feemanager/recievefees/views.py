import decimal

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_control
from rest_framework import status

from feemanager.managebalances.invoicedetails.models import BalanceTrackerDetails
from feemanager.managebalances.singleinvoicing.models import BalanceTracker
from feemanager.recievefeedetails.models import FeePaymentDetails
from feemanager.recievefees.models import FeePayment
from localities.models import Select2Data
from localities.serializers import Select2Serializer
from setups.academics.classes.models import SchoolClasses
from setups.academics.termdates.models import TermDates
from setups.accounts.bankbranches.models import BankBranches
from setups.accounts.paymentmodes.models import PaymentModes
from setups.accounts.standardcharges.models import StandardCharges
from setups.system.systemparameters.models import SystemParameters
from setups.system.systemsequences.models import SystemSequences
from studentmanager.student.models import Students
from useradmin.users.models import User

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def feepage(request):
    return render(request, 'fees/recievefees.html')

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

def searchstudents(request,id):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    students = Students.objects.raw(
        "SELECT top 5 student_code,adm_no,student_name from student_students where student_class_id=%s and ("+
        " adm_no like %s or student_name like %s)",
        [id, query,query])

    for obj in students:
        text = obj.student_name+'--'+obj.adm_no
        select2 = Select2Data()
        select2.id = str(obj.student_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})

def getfeestandardcharges(request):
    listsel = []
    charges = StandardCharges.objects.filter(charge_active=True).order_by('charge_priority')

    for charge in charges:
        response_data = {}
        response_data['chargeCode'] = charge.charge_code
        response_data['chargeCodeName'] = charge.charge_uiid + 'Value'
        response_data['chargeName'] = charge.charge_name
        response_data['chargeAmount'] = charge.charge_uiid + 'Amount'
        listsel.append(response_data)
    return JsonResponse(listsel, safe=False)

def getfeestudentcharges(request,id):
    listsel = []

    student = Students.objects.get(pk=id)
    tracker = BalanceTracker.objects.get(tracker_student=student)
    details = BalanceTrackerDetails.objects.filter(trackerdetails_tracker=tracker)

    for detail in details:
        charge = StandardCharges.objects.get(pk=detail.trackerdetails_Standardcharge.pk)
        response_data = {}
        response_data['chargeCode'] = charge.charge_code
        response_data['tracker'] = charge.charge_uiid+'TrackerCode'
        response_data['chargeCodeName'] = charge.charge_uiid + 'PaidValue'
        response_data['trackerCodeName'] = charge.charge_uiid + 'TrackerValue'
        response_data['chargeName'] = charge.charge_name
        response_data['chargeAmountName'] = charge.charge_uiid + 'PaidAmount'
        response_data['trackerCode']=detail.trackerdetails_code
        response_data['trackerAmountName']=charge.charge_uiid + 'TrackerAmount'
        response_data['trackerAmountValue']=detail.trackerdetails_balance

        listsel.append(response_data)

    return JsonResponse(listsel, safe=False)


def searchmodes(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    modes = PaymentModes.objects.raw(
        "SELECT top 5 payment_code,payment_name FROM paymentmodes_paymentmodes WHERE payment_name like %s or payment_desc like %s",
        tuple([query, query]))

    for obj in modes:
        text = obj.payment_name
        select2 = Select2Data()
        select2.id = str(obj.payment_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchbanks(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    branches = BankBranches.objects.raw(
        "SELECT top 5 bankbranch_code,bankbranch_name FROM bankbranches_bankbranches WHERE bankbranch_name like %s",
        tuple([query]))

    for obj in branches:
        text = obj.bankbranch_name
        select2 = Select2Data()
        select2.id = str(obj.bankbranch_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchterm(request):
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


def recievefees(request):
        stud = request.POST['student']
        cl = request.POST['classcode']
        md = request.POST['mode']
        bn = request.POST['bank']
        tr = request.POST['term']
        dt = request.POST['date']
        doc = request.POST['document']
        student = Students.objects.get(pk=stud)
        sclasses = SchoolClasses.objects.get(pk=cl)
        mode = PaymentModes.objects.get(pk=md)
        bank = BankBranches.objects.get(pk=bn)
        term = TermDates.objects.get(pk=tr)
        u = User.objects.get(username=request.user)
        receipt = ''
        if SystemSequences.objects.filter(sequence_type='Receipt').exists():
            seq = SystemSequences.objects.get(sequence_type='Receipt')
            receipt = 'RCT00' + str(seq.sequence_nextseq)
            seq.sequence_nextseq = seq.sequence_nextseq + 1
            seq.save()
        else:
            seq = SystemSequences()
            seq.sequence_nextseq = 1
            seq.sequence_type = 'Receipt'
            seq.save()
            receipt = 'RCT00' + str(seq.sequence_nextseq)
            seq.sequence_nextseq = seq.sequence_nextseq + 1
            seq.save()

        totals = 0
        payment = FeePayment()
        feex = FeePayment()
        pmnt = FeePayment()
        payment.payment_amount = totals
        payment.payment_bank = bank
        payment.payment_class = sclasses
        payment.payment_docno = doc
        payment.payment_term = term
        payment.payment_mode = mode
        payment.payment_receiptno = receipt
        payment.payment_student = student
        payment.payment_date = dt
        payment.payment_capturedby = u
        try:
            feex = FeePayment.objects.get(payment_docno=doc,payment_mode=mode)
        except feex.DoesNotExist:
            payment.save()
            pmnt = FeePayment.objects.get(pk=payment.pk)

        else:
            return JsonResponse({
                'error': 'Document number must be unique for each payment mode'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        for key in request.POST:

            if 'TrackerCode' in key:
                   feedet = FeePaymentDetails()
                   value = request.POST.get(key, None)
                   detailz = BalanceTrackerDetails.objects.get(pk=value)
                   charge = StandardCharges.objects.get(pk=detailz.trackerdetails_Standardcharge.pk)
                   chargename = charge.charge_uiid
                   paidamount = chargename + 'PaidAmount'
                   amount = request.POST.get(paidamount, None)
                   if not amount:
                     print('Amount is blank')
                   else:
                     print('Amount is empty')
                   if amount:

                     paymentdetail = FeePaymentDetails()
                     paymentdetail.paymentdetail_payment=pmnt
                     paymentdetail.paymentdetail_standardcharge=charge
                     paymentdetail.paymentdetailcharge_amount=decimal.Decimal(float(amount))
                     paymentdetail.save()
                     totals = totals + decimal.Decimal(float(amount))
                     amount = detailz.trackerdetails_balance-decimal.Decimal(float(amount))
                     detailz.trackerdetails_balance=amount
                     detailz.save()

        pmnt.payment_amount=totals
        pmnt.save()
        response_data = {}
        response_data['success'] = 'Record added Successfully!'
        response_data['amount'] = totals
        return JsonResponse(response_data)


def currentterm(request):
        response_data = {}
        obj = TermDates.objects.get(current_term=True)
        response_data['termCode'] = obj.term_code
        response_data['termNumber'] = obj.term_number
        return JsonResponse(response_data)


def feedistribution(request):
    parameter = SystemParameters()
    try:
        parameter = SystemParameters.objects.get(parameter_name='FEE_DISTRIBUTION_MODE')
    except parameter.DoesNotExist:
        return JsonResponse({
            'error': 'Setup parameter FEE_DISTRIBUTION_MODE ans assign it either a manual or automatic value'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        response_data={}
        response_data['mode']=parameter.parameter_value
        return JsonResponse(response_data)
