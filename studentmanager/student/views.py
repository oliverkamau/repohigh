from urllib.parse import urlsplit

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, request
from django.shortcuts import render
from datetime import datetime

# Create your views here.
from django.views.decorators.cache import cache_control

from feemanager.feesetup.feecategories.models import FeeCategories
from setups.academics.campuses.models import Campuses
from setups.academics.classes.models import SchoolClasses
from setups.academics.denominations.models import Denomination
from setups.academics.documents.models import Documents
from setups.academics.dorms.models import Dorms
from setups.academics.healthconditions.models import HealthStatus
from setups.academics.sources.models import StudentSources
from setups.academics.studentstatus.models import StudentStatus
from setups.academics.years.models import Years
from studentmanager.parents.models import Parents
from localities.models import Select2Data, Countries, Counties, SubCounty, Location, SubLocation, Village
from localities.serializers import Select2Serializer
from studentmanager.student.StudForm import StudForm
from studentmanager.student.models import Students

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
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
        "SELECT top 5 country_id,country_name FROM localities_countries WHERE country_name like %s or country_code like %s",
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
        "SELECT top 5 county_id,county_name FROM localities_counties WHERE county_country_id = %s and" +
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


def addstudent(request):
    student = StudForm(request.POST, request.FILES)
    # if request.method == 'POST':
    #     if 'parent_photo' in request.FILES:
    #         image = request.FILES.get('parent_photo')
    #         parent.parent_photo = image


    category = student.data['student_fee_category']
    dorm = student.data['student_dorm']
    campus = student.data['student_campus']
    sclass = student.data['student_class']
    parent = student.data['student_parent']
    nationality = student.data['nationality']
    county = student.data['student_county']
    subcounty = student.data['stud_sub_county']
    location = student.data['stud_location']
    sublocation = student.data['stud_sub_location']
    village = student.data['stud_village']
    denomination = student.data['student_denomination']
    sources = student.data['student_sources']
    healthstatus = student.data['health_status']
    studentstatus = student.data['student_status']

    if category is not None and category != '':
        cat = FeeCategories.objects.get(pk=category)
        student.student_fee_category = cat

    if dorm is not None and dorm != '':
        d = Dorms.objects.get(pk=dorm)
        student.student_dorm = d

    if campus is not None and campus != '':
        cam = Campuses.objects.get(pk=campus)
        student.student_campus = cam

    if sclass is not None and sclass != '':
        sass = SchoolClasses.objects.get(pk=sclass)
        student.student_class = sass

    if parent is not None and parent != '':
        par = Parents.objects.get(pk=parent)
        student.student_parent = par

    if nationality is not None and nationality != '':
        nt = Countries.objects.get(pk=nationality)
        student.nationality = nt

    if county is not None and county != '':
        ct = Counties.objects.get(pk=county)
        student.student_county = ct

    if subcounty is not None and subcounty != '':
        sct = SubCounty.objects.get(pk=subcounty)
        student.stud_sub_county = sct

    if location is not None and location != '':
        loc = Location.objects.get(pk=location)
        student.stud_location = loc

    if sublocation is not None and sublocation != '':
        sloc = SubLocation.objects.get(pk=sublocation)
        student.stud_sub_location = sloc

    if village is not None and village != '':
        vil = Village.objects.get(pk=village)
        student.stud_village = vil

    if denomination is not None and denomination != '':
        den = Denomination.objects.get(pk=denomination)
        student.student_denomination = den

    if sources is not None and sources != '':
        s = StudentSources.objects.get(pk=sources)
        student.student_sources = s

    if healthstatus is not None and healthstatus != '':
        health = HealthStatus.objects.get(pk=healthstatus)
        student.health_status = health

    if studentstatus is not None and studentstatus != '':
        stat = StudentStatus.objects.get(pk=studentstatus)
        student.student_status = stat

    print(student)
    inst=student.save()
    stud = Students.objects.get(pk=inst.pk)
    year = datetime.today().year
    year=str(year)
    year=year.replace('2','',1)
    year=year.replace('0','',2)
    keyuniq='S00'+str(stud.pk)+'/'+year
    stud.adm_no=keyuniq
    stud.save()
    return JsonResponse({'success': 'Student Saved Successfully'})


def getstudents(request):
    listsel = []
    students = Students.objects.raw(
        "SELECT top 20 student_code,adm_no,student_name,date_of_birth,adm_date,completion_date,dorm_name," +
        "class_name,student_email,student_phone,coalesce(father_name,mother_name)parent,student_gender,country_name FROM student_students" +
        " LEFT JOIN dorms_dorms ON student_dorm_id=dorm_code" +
        " LEFT JOIN classes_schoolclasses ON student_class_id=class_code" +
        " LEFT JOIN localities_countries ON nationality_id=country_id" +
        " LEFT JOIN parents_parents ON student_parent_id=parent_code"

    )

    for obj in students:
        if obj.student_code not in listsel:
            response_data = {}

            response_data['studentCode'] = obj.student_code
            response_data['name'] = obj.student_name
            response_data['admNo'] = obj.adm_no
            response_data['birthDate'] = obj.date_of_birth.strftime("%d/%m/%Y")
            response_data['admDate'] = obj.adm_date.strftime("%d/%m/%Y")
            response_data['completionDate'] = obj.completion_date.strftime("%d/%m/%Y")
            response_data['dorm'] = obj.dorm_name
            response_data['studentClass'] = obj.class_name
            response_data['email'] = obj.student_email
            response_data['phone'] = obj.student_phone
            response_data['parent'] = obj.parent
            response_data['nationality'] = obj.country_name

            if obj.student_gender == 'M':
                response_data['gender'] = "Male"
            elif obj.student_gender == 'F':
                response_data['gender'] = "Female"
            else:
                response_data['gender'] = "Other"

            listsel.append(response_data)

    return JsonResponse(listsel,safe=False)





def editstudent(request,id):

 student=Students.objects.raw("select student_code,student_name,adm_no,student_upi,student_gender,adm_term,"+
  "class_code,class_name,category_code,category_name,dorm_code,dorm_name,"+
  "campus_name,campus_code,parent_code,coalesce(father_name,mother_name)parent,"+
  "student_address,student_email,student_phone,parent_phone,country_id,country_name,"+
  "county_id,county_name,subcounty_name,subcounty_id,location_id,location_name,"+
  "sublocation_id,sublocation_name,village_id,village_name,completion_date,"+
  "adm_date,date_of_birth,birth_cert_no,index_no,grade,primary_school,marks,"+
  "denomination_code,denomination_name,studentsources_code,studentsources_name,"+
  "healthcondition_code,healthcondition_name,status_code,status_name,year_code,year_number"+
  " from student_students"+
  " left join classes_schoolclasses  on student_class_id = class_code"+
  " left join feecategories_feecategories on student_fee_category_id = category_code"+
  " left join dorms_dorms on student_dorm_id = dorm_code"+
  " left join campuses_campuses on student_campus_id = campus_code"+
  " left join parents_parents parent on student_parent_id = parent_code"+
  " left join localities_countries on nationality_id = country_id"+
  " left join localities_counties on student_county_id = county_id"+
  " left join localities_subcounty on stud_sub_county_id = subcounty_id"+
  " left join localities_location on stud_location_id = location_id"+
  " left join localities_sublocation on stud_sub_location_id = sublocation_id"+
  " left join localities_village on stud_village_id = village_id"+
  " left join denominations_denomination on student_denomination_id = denomination_code"+
  " left join sources_studentsources on student_sources_id = studentsources_code"+
  " left join healthconditions_healthstatus  on health_status_id = healthcondition_code"+
  " left join studentstatus_studentstatus on student_status_id = status_code"+
  " left join years_years  on student_exam_year_id = year_code"+
  " where student_code = %s",[id])
 listsel = []

 for obj in student:
    response_data = {}
    response_data['studentCode'] = obj.student_code
    response_data['name'] = obj.student_name
    response_data['admNo'] = obj.adm_no
    response_data['address'] = obj.student_address
    response_data['upi'] = obj.student_upi
    response_data['gender'] = obj.student_gender
    response_data['term'] = obj.adm_term
    response_data['birthDate'] = obj.date_of_birth.strftime("%Y-%m-%d")
    response_data['admDate'] = obj.adm_date.strftime("%Y-%m-%d")
    response_data['completionDate'] = obj.completion_date.strftime("%Y-%m-%d")
    response_data['dormCode'] = obj.dorm_code
    response_data['dormName'] = obj.dorm_name
    response_data['classCode'] = obj.class_code
    response_data['className'] = obj.class_name
    response_data['categoryCode'] = obj.category_code
    response_data['categoryName'] = obj.category_name
    response_data['parentCode'] = obj.parent_code
    response_data['parentName'] = obj.parent
    response_data['campusCode'] = obj.campus_code
    response_data['campusName'] = obj.campus_name
    response_data['email'] = obj.student_email
    response_data['phone'] = obj.student_phone
    response_data['parentPhone'] = obj.parent_phone
    response_data['marks'] = obj.marks
    response_data['grade'] = obj.grade
    response_data['primarySchool'] = obj.primary_school
    response_data['birthCertNo'] = obj.birth_cert_no
    response_data['indexNo'] = obj.index_no
    response_data['countryCode'] = obj.country_id
    response_data['countryName'] = obj.country_name
    response_data['countyCode'] = obj.county_id
    response_data['countyName'] = obj.county_name
    response_data['subCountyCode'] = obj.subcounty_id
    response_data['subCountyName'] = obj.subcounty_name
    response_data['locationCode'] = obj.location_id
    response_data['locationName'] = obj.location_name
    response_data['subLocationCode'] = obj.sublocation_id
    response_data['subLocationName'] = obj.sublocation_name
    response_data['villageCode'] = obj.village_id
    response_data['villageName'] = obj.village_name
    response_data['sourceCode'] = obj.studentsources_code
    response_data['sourceName'] = obj.studentsources_name
    response_data['healthCode'] = obj.healthcondition_code
    response_data['healthName'] = obj.healthcondition_name
    response_data['denominationCode'] = obj.denomination_code
    response_data['denominationName'] = obj.denomination_name
    response_data['statusCode'] = obj.status_code
    response_data['statusName'] = obj.status_name
    response_data['yearCode'] = obj.year_code
    response_data['yearName'] = str(obj.year_number)
    stud = Students.objects.get(pk=id)
    if stud.student_photo:
        response_data['url'] = urlsplit(request.build_absolute_uri(None)).scheme + '://' + request.get_host() + stud.student_photo.url
    listsel.append(response_data)


 return JsonResponse(listsel,safe=False)


def updatestudent(request,id):
    student = Students.objects.get(pk=id)
    form = StudForm(request.POST, request.FILES, instance=student)
    admnno = student.adm_no
    form.adm_no=admnno
    print(form)
    form.save()
    return JsonResponse({'success': 'Student Updated Successfully'})


def deletestudent(request,id):
    student=Students.objects.get(pk=id)
    student.delete()
    return JsonResponse({'success': 'Student Deleted Successfully'})
