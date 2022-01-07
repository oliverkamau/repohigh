import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime

# Create your views here.
from django.views.decorators.cache import cache_control
from rest_framework import status

from feemanager.feesetup.feecategories.models import FeeCategories
from feemanager.feesetup.feestructure.models import FeeStructure
from feemanager.feesetup.feestructuredetails.models import FeeStructureDetails
from localities.models import Select2Data
from localities.serializers import Select2Serializer
from setups.academics.termdates.models import TermDates
from setups.academics.years.models import Years
from setups.accounts.standardcharges.models import StandardCharges

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def structurepage(request):
    return render(request, 'fees/feestructure.html')

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

def searchfeecategory(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    categories = FeeCategories.objects.raw(
        "SELECT top 5 category_code,category_name FROM feecategories_feecategories WHERE category_name like %s or category_desc like %s",
        tuple([query, query]))

    for obj in categories:
        text = obj.category_name
        select2 = Select2Data()
        select2.id = str(obj.category_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def getfeestandardcharges(request):
    listsel=[]
    charges = StandardCharges.objects.filter(charge_active=True).order_by('charge_priority')

    for charge in charges:
        response_data = {}
        response_data['chargeCode']=charge.charge_code
        response_data['chargeCodeName']=charge.charge_uiid+'Value'
        response_data['chargeName']=charge.charge_name
        response_data['chargeAmount']=charge.charge_uiid+'Amount'
        listsel.append(response_data)
    return JsonResponse(listsel,safe=False)


def addfeestructure(request):
    fee = FeeStructure()
    feex = FeeStructure()
    fcharge = FeeStructure()
    if 'exam_term' in request.POST:
        t = request.POST['exam_term']
        term = TermDates.objects.get(pk=t)
        fee.structure_term = term
        y = datetime.today().year
        ys = str(y)
        year = Years.objects.get(year_number=int(ys))
        fee.structure_year = year
    if 'student_fee_category' in request.POST:
        fc = request.POST['student_fee_category']
        feecat = FeeCategories.objects.get(pk=fc)
        fee.structure_category = feecat
    try:
        feex = FeeStructure.objects.get(structure_category=fee.structure_category,structure_term=fee.structure_term,
                                        structure_year=fee.structure_year)
    except feex.DoesNotExist:
        fee.save()
        fcharge = FeeStructure.objects.get(pk=fee.structure_code)

    else:
        return JsonResponse({
                                'error': feex.structure_category.category_name + ' fee structure term' + feex.structure_term.term_number + ' for year ' + str(feex.structure_year.year_number)+ ' already defined'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    print(fcharge.structure_code)
    for key in request.POST:
        if key != 'student_fee_category' and key != 'exam_term':

           if 'Value' in key:
               details = FeeStructureDetails()
               value = request.POST[key]
               charge = StandardCharges.objects.get(pk=value)
               chargename=charge.charge_uiid
               chargeamount=chargename+'Amount'
               amount =  request.POST[chargeamount]
               details.structuredetail_ammount=amount
               details.structuredetail_Standardcharge=charge
               details.structuredetail_structure=fcharge
               details.save()


    return JsonResponse({'success':'Fee Structure Saved Successfully'})

def getfeestructures(request):
    feestructures = FeeStructure.objects.all()
    listsel = []
    for fee in feestructures:
        response_data = {}
        category = FeeCategories.objects.get(pk=fee.structure_category.pk)
        term = TermDates.objects.get(pk=fee.structure_term.pk)
        year = Years.objects.get(pk=fee.structure_year.pk)
        response_data['feeCategory']=category.category_name
        response_data['structureCode']=fee.structure_code
        response_data['feeTerm']=str(term.term_number)
        response_data['feeYear']=str(year.year_number)

        listsel.append(response_data)
    return JsonResponse(listsel,safe=False)


def editfeestructure(request,id):
    listsel = []
    structure = FeeStructure.objects.get(pk=id)
    term=TermDates.objects.get(pk=structure.structure_term.pk)
    category=FeeCategories.objects.get(pk=structure.structure_category.pk)
    details=FeeStructureDetails.objects.filter(structuredetail_structure=structure)
    for obj in details:
        response_data = {}
        charge = StandardCharges.objects.get(pk=obj.structuredetail_Standardcharge.pk)
        response_data['structureCode']=structure.structure_code
        response_data['termCode']=term.term_code
        response_data['termNumber']=str(term.term_number)
        response_data['categoryCode']=category.category_code
        response_data['categoryName']=category.category_name
        response_data['id']=charge.charge_uiid+'Amount'
        response_data['value']=str(obj.structuredetail_ammount)
        listsel.append(response_data)

    return JsonResponse(listsel,safe=False)


def updatefeestructure(request,id):
    structure = FeeStructure.objects.get(pk=id)
    if 'exam_term' in request.POST:
        t = request.POST['exam_term']
        term = TermDates.objects.get(pk=t)
        terms = structure.structure_term
        if term != terms:
            structure.structure_term=term
            y = datetime.today().year
            ys = str(y)
            year = Years.objects.get(year_number=int(ys))
            structure.structure_year = year

    if 'student_fee_category' in request.POST:
        fc = request.POST['student_fee_category']
        feecat = FeeCategories.objects.get(pk=fc)
        structure.structure_category = feecat

    structure.save()
    # detail = FeeStructureDetails.objects.filter(structuredetail_structure=structure.pk)
    #
    # for details in detail:
    #            charge = StandardCharges.objects.get(pk=details.structuredetail_Standardcharge.pk)
    #            chargename=charge.charge_uiid
    #            chargeamount=chargename+'Amount'
    #            amount =  request.POST[chargeamount]
    #            details.structuredetail_ammount=amount
    #            details.save()

    for key in request.POST:
        if key != 'student_fee_category' and key != 'exam_term':

           if 'Value' in key:
               detailz = FeeStructureDetails()
               feex = FeeStructureDetails()
               value = request.POST[key]
               charge = StandardCharges.objects.get(pk=value)
               chargename=charge.charge_uiid
               chargeamount=chargename+'Amount'
               amount =  request.POST[chargeamount]
               try:
                   feex = FeeStructureDetails.objects.get(structuredetail_structure=structure,
                                                          structuredetail_Standardcharge=charge)
               except feex.DoesNotExist:
                   detailz.structuredetail_ammount = amount
                   detailz.structuredetail_Standardcharge = charge
                   detailz.structuredetail_structure = structure
                   detailz.save()
               else:
                   feex.structuredetail_ammount=amount
                   feex.save()



    return JsonResponse({'success':'Fee Structure Updated Successfully'})

def deletefeestructure(request,id):
    structure = FeeStructure.objects.get(pk=id)
    detail = FeeStructureDetails.objects.filter(structuredetail_structure=structure.pk)
    for details in detail:
        details.delete()
    structure.delete()
    return JsonResponse({'success': 'Fee Structure Deleted Successfully'})
