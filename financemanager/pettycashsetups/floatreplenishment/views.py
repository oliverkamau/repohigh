import decimal

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_control

from financemanager.pettycashsetups.floatreplenishment.models import FloatReplenishment
from financemanager.pettycashsetups.pettycashbalances.models import PettyCashBalances
from localities.models import Select2Data
from localities.serializers import Select2Serializer
from setups.accounts.accountmaster.models import AccountMaster
from useradmin.users.models import User

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def replenishpage(request):
    return render(request,'finance/replenishfloat.html')

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


def balance(request,id):
    account = AccountMaster.objects.get(pk=id)
    response_data = {}

    if account.account_drcr == 'Cr':
        if account.account_balance != 0.00:
            if account.account_balance > 0.00:
               response_data['balance'] = '-'+str(account.account_balance)
            else:
               response_data['balance'] = account.account_balance
        else:
            response_data['balance'] = account.account_balance
    else:
        response_data['balance'] = account.account_balance

    return JsonResponse(response_data)


def float(request,id):
    response_data = {}
    petty = PettyCashBalances()
    user = User.objects.get(pk=id)
    try:
        petty = PettyCashBalances.objects.get(pettycashbalance_user=user)
    except petty.DoesNotExist:
        response_data['float']=0.00
    else:
        response_data['float']=petty.pettycashbalance_amount

    return JsonResponse(response_data)

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @login_required
def savefloatcash(request):
 if request.user.is_authenticated:
    payee = request.POST.get('float_givento', None)
    doc = request.POST.get('float_docno', None)
    acc = request.POST.get('cash_account', None)
    date = request.POST.get('float_date', None)
    amount = request.POST.get('float_amount', None)
    balance = request.POST.get('balance', None)
    payer = request.user

    userpayee = User.objects.get(pk=payee)
    userpayer = User.objects.get(username=payer)
    account = AccountMaster.objects.get(pk=acc)
    trap = 0.00
    petty = PettyCashBalances()
    try:
        petty = PettyCashBalances.objects.get(pettycashbalance_user=userpayee)
    except petty.DoesNotExist:
        cash = PettyCashBalances()
        cash.pettycashbalance_user = userpayee
        cash.pettycashbalance_amount = decimal.Decimal(amount)
        cash.save()
    else:
        trap = petty.pettycashbalance_amount
        petty.pettycashbalance_amount = petty.pettycashbalance_amount + decimal.Decimal(amount)
        petty.save()

    replenish = FloatReplenishment()
    replenish.float_account = account
    replenish.float_amount = decimal.Decimal(amount)
    replenish.float_assignee = userpayee
    replenish.float_assigner = userpayer
    replenish.float_docno = doc
    replenish.float_date = date
    replenish.float_runningbalance = decimal.Decimal(amount) + decimal.Decimal(balance)
    replenish.float_prevbal = account.account_balance
    replenish.float_accbal = trap
    replenish.save()

    account.account_balance = account.account_balance - decimal.Decimal(amount)
    account.save()

    return JsonResponse({'success':'Record created successfully!'})
 else:
    return JsonResponse({'timeout': 'Your User Session expired!!'})


def getfloatgrid(request):
    listsel = []
    floats = FloatReplenishment.objects.raw(
        "select top 100 float_code,float_date,float_amount,account_name,uu.username as givento,uv.username as givenby,float_docno,float_runningbalance from floatreplenishment_floatreplenishment" +
        " inner join accountmaster_accountmaster  on account_id = float_account_id" +
        " inner join users_user uu on uu.user_id = float_assignee_id" +
        " inner join users_user uv on uv.user_id = float_assigner_id" +
        " order by float_code desc"

    )
    for obj in floats:
        if obj.float_code not in listsel:
            response_data = {}

            response_data['code'] = obj.float_code
            response_data['date'] = obj.float_date.strftime('%d/%m/%Y')
            response_data['amount'] = obj.float_amount
            response_data['balance'] = obj.float_runningbalance
            response_data['account'] = obj.account_name
            response_data['givenby'] = obj.givenby
            response_data['givento'] = obj.givento
            response_data['docno'] = obj.float_docno

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)

def geteditfloat(request,id):

    obj = FloatReplenishment.objects.get(pk=id)
    userpayee = User.objects.get(pk=obj.float_assignee.pk)
    userpayer = User.objects.get(pk=obj.float_assigner.pk)
    account = AccountMaster.objects.get(pk=obj.float_account.pk)
    petty = PettyCashBalances.objects.get(pettycashbalance_user=userpayee)
    response_data = {}
    response_data['code'] = obj.float_code
    response_data['accountBalance'] = account.account_balance
    response_data['date'] = obj.float_date.strftime('%Y-%m-%d')
    response_data['amount'] = obj.float_amount
    response_data['balance'] = petty.pettycashbalance_amount
    response_data['accountCode'] = account.account_id
    response_data['accountName'] = account.account_name
    response_data['givenbyCode'] = userpayer.user_id
    response_data['givenbyName'] = userpayer.username
    response_data['giventoCode'] = userpayee.user_id
    response_data['giventoName'] = userpayee.username
    response_data['docno'] = obj.float_docno

    return JsonResponse(response_data)
