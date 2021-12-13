from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from exams.examtype.models import ExamType
from exams.registration.forms import ExamRegForm
from exams.registration.models import ExamRegistration
from localities.models import Select2Data
from localities.serializers import Select2Serializer
from setups.academics.gradingschemes.models import GradingSchemes
from setups.academics.gradingsystem.models import GradingSystem
from setups.academics.termdates.models import TermDates
from setups.academics.years.models import Years


def examreg(request):
    return render(request,'exams/examregistration.html')

def searchexamtype(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    exams = ExamType.objects.raw(
        "SELECT top 5 type_code,type_name FROM examtype_examtype WHERE type_name like %s or type_desc like %s",
        tuple([query, query]))

    for obj in exams:
        select2 = Select2Data()
        select2.id = str(obj.type_code)
        select2.text = obj.type_name
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchexamterm(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    terms = TermDates.objects.raw(
        "SELECT top 5 term_code,term_number FROM termdates_termdates WHERE term_number like %s",
        [query])

    for obj in terms:
        select2 = Select2Data()
        select2.id = str(obj.term_code)
        select2.text = obj.term_number
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchexamgrading(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    grading = GradingSchemes.objects.raw(
        "SELECT top 5 scheme_code,scheme_name FROM gradingschemes_gradingschemes WHERE scheme_name like %s",
        [query])

    for obj in grading:
        select2 = Select2Data()
        select2.id = str(obj.scheme_code)
        select2.text = obj.scheme_name
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


def createexamreg(request):
    final=''
    combined=''
    if request.method == 'POST' and 'final_exam' in request.POST:
        val = request.POST['final_exam']
        final = val
    else:
        final = ''

    if request.method == 'POST' and 'combined_exam' in request.POST:
        val = request.POST['combined_exam']
        combined = val
    else:
        combined = ''

    exam = ExamRegForm(request.POST)
    # if request.method == 'POST':
    #     if 'parent_photo' in request.FILES:
    #         image = request.FILES.get('parent_photo')
    #         parent.parent_photo = image

    et = exam.data['exam_type']
    ey = exam.data['exam_year']
    etr = exam.data['exam_term']
    eg = exam.data['exam_grade_scheme']

    if et is not None and et != '':
        type = ExamType.objects.get(pk=et)
        exam.exam_type = type

    if ey is not None and ey != '':
        yr = Years.objects.get(pk=ey)
        exam.exam_year = yr

    if etr is not None and etr != '':
        trm = TermDates.objects.get(pk=etr)
        exam.exam_term = trm

    if eg is not None and eg != '':
        grade = GradingSchemes.objects.get(pk=eg)
        exam.exam_grade_scheme = grade


    if final is not None and final == 'on':
        exam.final_exam = True
    else:
        exam.final_exam = False

    if combined is not None and combined == 'on':
        exam.combined_exam = True
    else:
        exam.combined_exam = False

    exam.save()
    return JsonResponse({'success': 'Exam Registered Successfully'})


def getexamreg(request):

    listsel = []

    regs = ExamRegistration.objects.raw(
        "select top 100 exam_reg_code,exam_status,exam_national, month, display_name, effective_date, final_exam, combined_exam, lock_date, scheme_name, term_number, year_number, type_name, exam_name from registration_examregistration" +
        " inner join examtype_examtype  on exam_type_id = type_code"+
        " inner join gradingschemes_gradingschemes  on exam_grade_scheme_id = scheme_code" +
        " inner join years_years on exam_year_id = year_code"+
        " inner join termdates_termdates on exam_term_id = term_code")

    for obj in regs:
        response_data = {}
        response_data['regCode'] = obj.exam_reg_code
        response_data['month'] = obj.month
        response_data['displayName'] = obj.display_name
        response_data['examName'] = obj.exam_name
        response_data['finalExam'] = obj.final_exam
        response_data['combinedExam'] = obj.combined_exam
        response_data['termNumber'] = obj.term_number
        response_data['effectiveDate'] = obj.effective_date.strftime("%d/%m/%Y")
        response_data['lockDate'] = obj.lock_date.strftime("%d/%m/%Y")
        response_data['gradingName'] = obj.scheme_name
        response_data['typeName'] = obj.type_name
        response_data['yearNumber'] = obj.year_number
        response_data['status'] = obj.exam_status
        response_data['national'] = obj.exam_national

        listsel.append(response_data)

    return JsonResponse(listsel, safe=False)


def editexamreg(request,id):
    response_data = {}
    examreg = ExamRegistration.objects.get(pk=id)
    if examreg.exam_term is not None:
        tm = TermDates.objects.get(pk=examreg.exam_term.pk)
        response_data['termCode'] = tm.term_code
        response_data['termNumber'] = tm.term_number

    if examreg.exam_year is not None:
        yr = Years.objects.get(pk=examreg.exam_year.pk)
        response_data['yearCode'] = yr.year_code
        response_data['yearNumber'] = yr.year_number

    if examreg.exam_grade_scheme is not None:
        gr = GradingSchemes.objects.get(pk=examreg.exam_grade_scheme.pk)
        response_data['gradeCode'] = gr.scheme_code
        response_data['gradeName'] = gr.scheme_name

    if examreg.exam_type is not None:
        ty = ExamType.objects.get(pk=examreg.exam_type.pk)
        response_data['typeCode'] = ty.type_code
        response_data['typeName'] = ty.type_name

    response_data['regCode'] = examreg.exam_reg_code
    response_data['month'] = examreg.month
    response_data['displayName'] = examreg.display_name
    response_data['examName'] = examreg.exam_name
    response_data['finalExam'] = examreg.final_exam
    response_data['combinedExam'] = examreg.combined_exam


    if examreg.effective_date:
        response_data['effectiveDate'] = examreg.effective_date.strftime("%Y-%m-%d")

    if examreg.lock_date:
        response_data['lockDate'] = examreg.lock_date.strftime("%Y-%m-%d")


    return JsonResponse(response_data)


def updateregister(request,id):
    examreg = ExamRegistration.objects.get(pk=id)

    form = ExamRegForm(request.POST, instance=examreg)

    form.save()
    return JsonResponse({'success': 'Exam Updated Successfully'})


def deleteexam(request,id):
    examreg = ExamRegistration.objects.get(pk=id)
    examreg.delete()
    return JsonResponse({'success': 'Exam Deleted Successfully'})
