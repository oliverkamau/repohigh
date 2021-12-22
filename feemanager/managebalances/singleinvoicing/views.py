from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from feemanager.managebalances.invoicedetails.models import BalanceTrackerDetails
from feemanager.managebalances.singleinvoicing.models import BalanceTracker
from localities.models import Select2Data
from localities.serializers import Select2Serializer
from setups.accounts.standardcharges.models import StandardCharges
from setups.system.invoicesequence.models import InvoiceSequence
from setups.system.systemsequences.models import SystemSequences
from studentmanager.student.models import Students


def singleinvoicepage(request):
    return render(request, 'fees/singleinvoicing.html')


def searchstudents(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    students = Students.objects.raw(
        "SELECT top 5 student_code,concat(adm_no,'--',student_name)name FROM student_students WHERE adm_no like %s or student_name like %s",
        [query, query])

    for obj in students:
        text = obj.name
        select2 = Select2Data()
        select2.id = str(obj.student_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})

def getfeestandardcharges(request,id):
    listsel=[]
    student = Students.objects.get(pk=id)
    tracker = BalanceTracker.objects.get(tracker_student=student)
    charges = BalanceTrackerDetails.objects.filter(trackerdetails_tracker=tracker)
    for charge in charges:
        standardcharge = StandardCharges.objects.get(pk=charge.trackerdetails_Standardcharge.pk)
        response_data = {}
        response_data['trackerCode']=tracker.pk
        response_data['chargeCode']=standardcharge.pk
        response_data['chargeCodeName']=standardcharge.charge_uiid+'Value'
        response_data['chargeName']=standardcharge.charge_name
        response_data['chargeAmount']=standardcharge.charge_uiid+'Amount'
        response_data['ammount']=charge.trackerdetails_balance
        listsel.append(response_data)
    return JsonResponse(listsel,safe=False)


def updatebalancetracker(request):
    tracker = BalanceTracker()
    if 'tracker_code' in request.POST:
        bal = request.POST['tracker_code']
        tracker = BalanceTracker.objects.get(pk=bal)
        tracker.tracker_notes=request.POST['notes']
        tracker.tracker_date=request.POST['date']
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

    for key in request.POST:
        if key != 'student_fee_category' and key != 'exam_term':

            if 'Value' in key:
                detailz = BalanceTrackerDetails()
                feex = BalanceTrackerDetails()
                value = request.POST[key]
                charge = StandardCharges.objects.get(pk=value)
                chargename = charge.charge_uiid
                chargeamount = chargename + 'Amount'
                amount = request.POST[chargeamount]
                try:
                    feex = BalanceTrackerDetails.objects.get(trackerdetails_tracker=tracker,
                                                           trackerdetails_Standardcharge=charge)
                except feex.DoesNotExist:
                    detailz.trackerdetails_balance = amount
                    detailz.trackerdetails_Standardcharge = charge
                    detailz.trackerdetails_tracker = tracker
                    detailz.save()
                else:
                    feex.trackerdetails_balance = amount
                    feex.save()


    return JsonResponse({'success':'Balance Updated Successfully'})