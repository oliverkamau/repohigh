import decimal

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status

from financemanager.pettycashsetups.pettycashbalances.models import PettyCashBalances
from financemanager.pettycashsetups.pettycashpayments.models import PettyCashPayments
from localities.models import Select2Data
from localities.serializers import Select2Serializer
from setups.accounts.accountmaster.models import AccountMaster
from setups.system.systemsequences.models import SystemSequences
from useradmin.users.models import User


def paymentpage(request):
    return render(request,'finance/pettycashpayment.html')


def searchaccount(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    accounts = AccountMaster.objects.raw(
        "SELECT top 5 account_id,account_name FROM accountmaster_accountmaster WHERE account_name like %s",
        [query])

    for obj in accounts:
        select2 = Select2Data()
        select2.id = str(obj.account_id)
        select2.text = obj.account_name
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchusers(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    users = User.objects.raw(
        "SELECT top 5 user_id,username FROM users_user WHERE username like %s",
        [query])

    for obj in users:
        select2 = Select2Data()
        select2.id = str(obj.user_id)
        select2.text = obj.username
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def savepettycash(request):
    payee = request.POST.get('pettycash_payee', None)
    doc = request.POST.get('pettycashdoc_no', None)
    acc = request.POST.get('pettycash_account', None)
    words = request.POST.get('pettycash_amountwording', None)
    date = request.POST.get('pettycash_date', None)
    amount = request.POST.get('pettycash_amount', None)
    trans = request.POST.get('pettycash_transdescription', None)
    payer = request.POST.get('pettycash_paidby', None)
    payers = User.objects.get(user_id=payer)
    account = AccountMaster.objects.get(pk=acc)
    petty = PettyCashBalances()
    try:
        petty = PettyCashBalances.objects.get(pettycashbalance_user=payers)
    except petty.DoesNotExist:
        return JsonResponse({
            'error': 'This user has zero float so go and replenish his float to continue!'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        if petty.pettycashbalance_amount < decimal.Decimal(amount):
            return JsonResponse({
                'error': 'The user has insufficient float replenish to continue!'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            petty.pettycashbalance_amount = petty.pettycashbalance_amount - decimal.Decimal(amount)
            petty.save()

    payments = PettyCashPayments()
    payments.pettycash_account = account
    payments.pettycash_amount = decimal.Decimal(amount)
    payments.pettycash_date = date
    payments.pettycash_payee = payee
    payments.pettycash_amountwording = words
    payments.pettycashdoc_no = doc
    payments.pettycash_paidby = payers
    payments.pettycash_transdescription = trans

    invoice = ''
    if SystemSequences.objects.filter(sequence_type='Invoice').exists():
        seq = SystemSequences.objects.get(sequence_type='Invoice')
        invoice = 'INV00' + str(seq.sequence_nextseq)
        seq.sequence_nextseq = seq.sequence_nextseq + 1
        seq.save()
    else:
        seq = SystemSequences()
        seq.sequence_nextseq = 1
        seq.sequence_type = 'Invoice'
        seq.save()
        invoice = 'INV00' + str(seq.sequence_nextseq)
        seq.sequence_nextseq = seq.sequence_nextseq + 1
        seq.save()
   
    payments.pettycash_voucherno = invoice
    payments.pettycash_receiptno = doc
    payments.save()
    
    return JsonResponse({'success':'Record Saved Successfully!'})


def getpettycashgrid(request):
    listsel = []
    payments = PettyCashPayments.objects.raw(
        "select top 100 pettycash_code,pettycash_date,pettycash_amount,pettycash_amountwording,pettycash_payee,username,pettycash_transdescription,pettycash_voucherno,pettycash_receiptno,account_name from pettycashpayments_pettycashpayments" +
        " inner join accountmaster_accountmaster on account_id = pettycash_account_id" +
        " inner join users_user  on user_id = pettycash_paidby_id" +
        " order by pettycash_code desc"

    )
    for obj in payments:
        if obj.pettycash_code not in listsel:
            response_data = {}

            response_data['code'] = obj.pettycash_code
            response_data['date'] = obj.pettycash_date.strftime('%d/%m/%Y')
            response_data['amount'] = obj.pettycash_amount
            response_data['wording'] = obj.pettycash_amountwording
            response_data['account'] = obj.account_name
            response_data['purpose'] = obj.pettycash_transdescription
            response_data['payee'] = obj.pettycash_payee
            response_data['payer'] = obj.username
            response_data['trans'] = obj.pettycash_transdescription
            response_data['voucher'] = obj.pettycash_voucherno
            response_data['receipt'] = obj.pettycash_receiptno

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)


def geteditpetty(request,id):
    obj = PettyCashPayments.objects.get(pk=id)
    userpayer = User.objects.get(pk=obj.pettycash_paidby.pk)
    account = AccountMaster.objects.get(pk=obj.pettycash_account.pk)
    response_data = {}
    response_data['code'] = obj.pettycash_code
    response_data['date'] = obj.pettycash_date.strftime('%Y-%m-%d')
    response_data['amount'] = obj.pettycash_amount
    response_data['wording'] = obj.pettycash_amountwording
    response_data['payee'] = obj.pettycash_payee
    response_data['trans'] = obj.pettycash_transdescription
    response_data['accountCode'] = account.account_id
    response_data['accountName'] = account.account_name
    response_data['givenbyCode'] = userpayer.user_id
    response_data['givenbyName'] = userpayer.username
    response_data['docno'] = obj.pettycash_receiptno

    return JsonResponse(response_data)