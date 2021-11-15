import math
import os
from io import BytesIO
from math import nan
from urllib.parse import urlsplit, urlparse

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import pandas as pd

# Create your views here.
from django.views.decorators.cache import cache_control
from rest_framework import status

from studentmanager.parents.forms import ParentsForm
from studentmanager.parents.models import Parents, ExcelFile
from studentmanager.parents.proffessions.models import Proffessions
from localities.models import Select2Data
from localities.serializers import Select2Serializer
from django.conf import Settings, settings

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def getparent(request):
    return render(request,'students/parents.html')


def searchproffession(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    profs = Proffessions.objects.raw(
        "SELECT TOP 5 proffesion_id,proffesion_name FROM proffessions_proffessions WHERE proffessions_proffessions.proffesion_name LIKE %s OR proffessions_proffessions.proffesion_desc LIKE %s",
        tuple([query, query]))

    for obj in profs:
        select2 = Select2Data()
        select2.id = str(obj.proffesion_id)
        select2.text = obj.proffesion_name
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})

def importexcel(request):
    if request.method == 'POST':
        file = request.FILES['file']
        obj = ExcelFile.objects.create(
            file = file
        )
        path = str(obj.file.path)

        print('path here...')
        print(path)
        df=pd.read_excel(path)
        print(df)
        th=df.to_dict('records')
        for obj in th:
           print(obj)
            # null=nan
           parent=Parents()
           if obj['FatherName'] != 'nan':
              parent.father_name=obj['FatherName']
           print(obj['FatherAddress'])
           print(str(obj['FatherAddress']))
           if str(obj['FatherAddress']) != 'nan':
              parent.father_address = obj['FatherAddress']

           if str(obj['FatherPhone']) != 'nan':
              parent.father_phone = obj['FatherPhone']
           if str(obj['IDNO']) != 'nan':
              parent.id_no = obj['IDNO']
           if str(obj['FatherEmail']) != 'nan':
              parent.father_email = obj['FatherEmail']
           if str(obj['MotherAddress']) != 'nan':
              parent.mother_address = obj['MotherAddress']
           if str(obj['MotherPhone']) != 'nan':
              parent.mother_phone = obj['MotherPhone']
           if str(obj['MotherEmail']) != 'nan':
              parent.mother_email = obj['MotherEmail']
           if str(obj['ParentOrGuardian']) != 'nan':
               if obj['ParentOrGuardian'] == 'Parent':
                   parent.parent_type = 'P'
               else:
                   parent.parent_type='G'
           if str(obj['EmailRequired']) != 'nan':
               if obj['EmailRequired'] == 'Yes':
                   parent.email_required = True
               else:
                   parent.email_required= False

           # do error pass to json response
           # save batch
           if str(obj['FatherProffession']) != 'nan':
              # proffession = Proffessions.objects.get(proffesion_name=obj['FatherProffession'])
              try:
                  proffession = Proffessions.objects.get(proffesion_name=obj['FatherProffession'])
                  parent.father_proffession = proffession
              except Proffessions.DoesNotExist:
                  return JsonResponse({'error': str(obj['FatherProffession']) + ' is not defined'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

           if str(obj['MotherProffession']) != 'nan':
               try:
                   proffession = Proffessions.objects.get(proffesion_name=obj['MotherProffession'])
                   parent.mother_proffession = proffession

               except Proffessions.DoesNotExist:
                   return JsonResponse({'error': str(obj['MotherProffession'])+' is not defined'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

           parent.save()

        return JsonResponse({'success': 'Parents Imported Successfully'})


def get_parentsData():
     pr=Parents.objects.raw("select parent_code,father_name,father_address,father_phone,"+
                            "father_email,id_no,f.proffesion_name as fatherProfName,"+
                            "parent_type,email_required,mother_name,"+
                            "mother_address,mother_phone,mother_email,"+
                            "m.proffesion_name as motherProfName from parents_parents"+
                            " left join proffessions_proffessions f on father_proffession_id=f.proffesion_id"+
                            " left join proffessions_proffessions m on mother_proffession_id=m.proffesion_id")
     listsel=[]
     for obj in pr:
         if obj.parent_code not in listsel:
             response_data = {}

             response_data['ParentCode'] = obj.parent_code
             response_data['FatherName'] = obj.father_name
             response_data['MotherName'] = obj.mother_name
             response_data['FatherAddress'] = obj.father_address
             response_data['MotherAddress'] = obj.mother_address
             response_data['IdNo'] = obj.id_no
             response_data['FatherPhone'] = obj.father_phone
             response_data['MotherPhone'] = obj.mother_phone
             response_data['FatherEmail'] = obj.father_email
             response_data['MotherEmail'] = obj.mother_email
             response_data['EmailRequired'] = obj.email_required

             if obj.parent_type == 'P':
                 response_data['ParentType'] = "Parent"
             else:
                 response_data['ParentType'] = "Guardian"

             if obj.fatherProfName is None:
                 response_data['FatherProfName'] = "Not Availed"
             else:
                 response_data['FatherProfName'] = obj.fatherProfName

             if obj.motherProfName is None:
                 response_data['MotherProfName'] = "Not Availed"
             else:
                 response_data['MotherProfName'] = obj.motherProfName

             listsel.append(response_data)


     # df = pd.DataFrame(listsel, columns=['Code','FatherName', 'FatherAddress','FatherPhone','FatherEmail','IDNO','FatherProffession','ParentOrGuardian',
     #                                'EmailRequired','MotherName','MotherAddress','MotherPhone','MotherEmail','MotherProffession'])
     df = pd.DataFrame(listsel)
     print(df)
     return df


def generateExcel(request):
        with BytesIO() as b:
            data = get_parentsData()

            with pd.ExcelWriter(b) as writer:
                data.to_excel(writer, sheet_name="Data", index=False)


            filename = f"parentsdata.xlsx"
            res = HttpResponse(
                b.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            res['Content-Disposition'] = f'attachment; filename={filename}'
            return res

def addparents(request):
    email_req = ''
    if request.method == 'POST' and 'email_required' in request.POST:
        val = request.POST['email_required']
        email_req = val
    else:
        email_req = ''
    parent = ParentsForm(request.POST,request.FILES)
    # if request.method == 'POST':
    #     if 'parent_photo' in request.FILES:
    #         image = request.FILES.get('parent_photo')
    #         parent.parent_photo = image

    mp = parent.data['mother_proffession']
    fp = parent.data['father_proffession']

    if mp is not None and mp != '':
        motherProf = Proffessions.objects.get(pk=mp)
        parent.mother_proffession = motherProf

    if fp is not None and fp != '':
        fatherProf = Proffessions.objects.get(pk=fp)
        parent.father_proffession = fatherProf

    if email_req is not None and email_req == 'on':
        parent.email_required = True
    else:
        parent.email_required = False

    parent.save()
    return JsonResponse({'success': 'Parent Saved Successfully'})


def editparents(request,id):
    parent = Parents.objects.get(pk=id)
    response_data = {}
    if parent.father_proffession is not None:
       fprof = Proffessions.objects.get(pk=parent.father_proffession.pk)
       response_data['fatherProfId'] = fprof.proffesion_id
       response_data['fatherProfName'] = fprof.proffesion_name

    if parent.mother_proffession is not None:
        mprof = Proffessions.objects.get(pk=parent.mother_proffession.pk)
        response_data['motherProfId'] = mprof.proffesion_id
        response_data['motherProfName'] = mprof.proffesion_name

    response_data['parentCode'] = parent.parent_code
    response_data['fatherName'] = parent.father_name
    response_data['motherName'] = parent.mother_name
    response_data['fatherAddress'] = parent.father_address
    response_data['motherAddress'] = parent.mother_address
    response_data['idNo'] = parent.id_no
    response_data['fatherPhone'] = parent.father_phone
    response_data['motherPhone'] = parent.mother_phone
    response_data['fatherEmail'] = parent.father_email
    response_data['motherEmail'] = parent.mother_email
    # response_data['parentType'] = obj.parent_type
    response_data['emailRequired'] = parent.email_required

    response_data['parentType'] = parent.parent_type


    # if not parent.parent_photo:
    #    print('File Absent')
    # else:
    #    print('File Present')
    # url = request.get_host() + parent.parent_photo.url
    # print(urlsplit(request.build_absolute_uri(None)).scheme)

    if parent.parent_photo:
        response_data['url'] = urlsplit(request.build_absolute_uri(None)).scheme + '://' + request.get_host() + parent.parent_photo.url
    return JsonResponse(response_data)


def updateparents(request,id):
    parents = Parents.objects.get(pk=id)

    form = ParentsForm(request.POST,request.FILES, instance=parents)
    # if request.method == 'POST':
    #     if 'parent_photo' in request.FILES:
    #         image = request.FILES.get('parent_photo')
    #         print(image)
    #         form.parent_photo = image
    form.save()
    return JsonResponse({'success': 'Parent Updated Successfully'})


def deleteparents(request,id):
    parents = Parents.objects.get(pk=id)
    parents.delete()
    return JsonResponse({'success': 'Parent Deleted Successfully'})


def getparents(request):
    listsel = []
    parents = Parents.objects.raw(
        "SELECT parent_code,father_name,mother_name,father_address,mother_address,id_no,father_phone,mother_phone,father_email," +
        "mother_email,parent_type,email_required,f.proffesion_name as fatherProfName,f.proffesion_id as fatherProfId,m.proffesion_name as motherProfName,m.proffesion_id as motherProfId FROM parents_parents" +
        " LEFT JOIN  proffessions_proffessions f ON father_proffession_id=f.proffesion_id" +
        " LEFT JOIN proffessions_proffessions m ON mother_proffession_id=m.proffesion_id")

    for obj in parents:
        if obj.parent_code not in listsel:
            response_data = {}

            response_data['parentCode'] = obj.parent_code
            response_data['fatherName'] = obj.father_name
            response_data['motherName'] = obj.mother_name
            response_data['fatherAddress'] = obj.father_address
            response_data['motherAddress'] = obj.mother_address
            response_data['idNo'] = obj.id_no
            response_data['fatherPhone'] = obj.father_phone
            response_data['motherPhone'] = obj.mother_phone
            response_data['fatherEmail'] = obj.father_email
            response_data['motherEmail'] = obj.mother_email
            # response_data['parentType'] = obj.parent_type
            response_data['emailRequired'] = obj.email_required

            if obj.parent_type == 'P' :
                response_data['parentType'] = "Parent"
            else:
                response_data['parentType'] = "Guardian"

            if obj.fatherProfName is None:
                response_data['fatherProfName'] = "Not Availed"
            else:
                response_data['fatherProfName'] = obj.fatherProfName

            if obj.motherProfName is None:
                response_data['motherProfName'] = "Not Availed"
            else:
                response_data['motherProfName'] = obj.motherProfName

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)