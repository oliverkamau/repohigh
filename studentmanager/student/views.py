from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from feemanager.feesetup.feecategories.models import FeeCategories
from setups.academics.campuses.models import Campuses
from setups.academics.classes.models import SchoolClasses
from setups.academics.denominations.models import Denomination
from setups.academics.documents.models import Documents
from setups.academics.dorms.models import Dorms
from setups.academics.healthconditions.models import HealthStatus
from setups.academics.sources.models import StudentSources
from setups.academics.studentstatus.models import StudentStatus
from setups.academics.termdates.models import TermDates
from setups.academics.years.models import Years
from studentmanager.parents.models import Parents
from localities.models import Select2Data, Countries, Counties, SubCounty, Location, SubLocation, Village
from localities.serializers import Select2Serializer


def studentpage(request):
    return render(request,'students/studentsdetail.html')

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


def searchparent(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    parents = Parents.objects.raw(
        "SELECT top 5 parent_code,coalesce(father_name,mother_name)name FROM parents_parents WHERE father_name like %s or mother_name like %s",
        tuple([query, query]))

    for obj in parents:
        text = obj.name
        select2 = Select2Data()
        select2.id = str(obj.parent_code)
        select2.text = text
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

def searchdorms(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    dorms = Dorms.objects.raw(
        "SELECT top 5 dorm_code,dorm_name FROM dorms_dorms WHERE dorm_name like %s",
        tuple([query]))

    for obj in dorms:
        text = obj.dorm_name
        select2 = Select2Data()
        select2.id = str(obj.dorm_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchcampus(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    campuses = Campuses.objects.raw(
        "SELECT top 5 campus_code,campus_name FROM campuses_campuses WHERE campus_name like %s",
        tuple([query]))

    for obj in campuses:
        text = obj.campus_name
        select2 = Select2Data()
        select2.id = str(obj.campus_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchcountry(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    students = Countries.objects.raw(
        "SELECT top 5 country_id,country_name FROM students_countries WHERE country_name like %s or country_code like %s",
        tuple([query, query]))

    for obj in students:
        text = obj.country_name
        select2 = Select2Data()
        select2.id = str(obj.country_id)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})

def searchcounties(request,id):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    counties = Counties.objects.raw(
        "SELECT top 5 county_id,county_name FROM students_counties WHERE county_country_id = %s and" +
        " (county_name like %s or county_code like %s)",
        [id, query,query])

    for obj in counties:
        text = obj.county_name
        select2 = Select2Data()
        select2.id = str(obj.county_id)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchsubcounty(request,id):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    subcounties = SubCounty.objects.raw(
        "SELECT top 5 subcounty_id,subcounty_name FROM localities_subcounty WHERE subcounty_county_id = %s and" +
        " (subcounty_name like %s or subcounty_code like %s)",
        [id, query,query])

    for obj in subcounties:
        text = obj.subcounty_name
        select2 = Select2Data()
        select2.id = str(obj.subcounty_id)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchlocation(request,id):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    locations = Location.objects.raw(
        "SELECT top 5 location_id,location_name FROM localities_location WHERE location_subcounty_id = %s and" +
        " (location_name like %s or location_code like %s)",
        [id, query,query])

    for obj in locations:
        text = obj.location_name
        select2 = Select2Data()
        select2.id = str(obj.location_id)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchsublocation(request,id):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    sublocations = SubLocation.objects.raw(
        "SELECT top 5 sublocation_id,sublocation_name FROM localities_sublocation WHERE sublocation_location_id = %s and" +
        " (sublocation_name like %s or sublocation_code like %s)",
        [id, query,query])

    for obj in sublocations:
        text = obj.sublocation_name
        select2 = Select2Data()
        select2.id = str(obj.sublocation_id)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})

def searchvillage(request,id):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    villages = Village.objects.raw(
        "SELECT top 5 village_id,village_name FROM localities_village WHERE village_sublocation_id = %s and" +
        " (village_name like %s or village_code like %s)",
        [id, query,query])

    for obj in villages:
        text = obj.village_name
        select2 = Select2Data()
        select2.id = str(obj.village_id)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchdenominations(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    denominations = Denomination.objects.raw(
        "SELECT top 5 denomination_code,denomination_name FROM denominations_denomination WHERE denomination_name like %s",
        tuple([query]))

    for obj in denominations:
        text = obj.denomination_name
        select2 = Select2Data()
        select2.id = str(obj.denomination_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchstudentsources(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    sources = StudentSources.objects.raw(
        "SELECT top 5 studentsources_code,studentsources_name FROM sources_studentsources WHERE studentsources_name like %s",
        tuple([query]))

    for obj in sources:
        text = obj.studentsources_name
        select2 = Select2Data()
        select2.id = str(obj.studentsources_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchyears(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    sources = Years.objects.raw(
        "SELECT top 5 year_code,year_number FROM years_years WHERE year_number like %s or year_name like %s",
        tuple([query,query]))

    for obj in sources:
        text = str(obj.year_number)
        select2 = Select2Data()
        select2.id = str(obj.year_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchstudentstatus(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    statuses = StudentStatus.objects.raw(
        "SELECT top 5 status_code,status_name FROM studentstatus_studentstatus WHERE status_name like %s",
        tuple([query]))

    for obj in statuses:
        text = obj.status_name
        select2 = Select2Data()
        select2.id = str(obj.status_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchhealthstatus(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    statuses = HealthStatus.objects.raw(
        "SELECT top 5 healthcondition_code,healthcondition_name FROM healthconditions_healthstatus WHERE healthcondition_name like %s",
        tuple([query]))

    for obj in statuses:
        text = obj.healthcondition_name
        select2 = Select2Data()
        select2.id = str(obj.healthcondition_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchdocs(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    documents = Documents.objects.raw(
        "SELECT top 5 document_code,document_name FROM documents_documents WHERE document_name like %s",
        tuple([query]))

    for obj in documents:
        text = obj.document_name
        select2 = Select2Data()
        select2.id = str(obj.document_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})