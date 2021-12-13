from io import BytesIO
from urllib.parse import urlsplit

from django.db import connection
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import pandas as pd
from datetime import datetime

# Create your views here.
from rest_framework import status

from exams.processing.forms import ProcessingForm
from exams.processing.models import ExamProcessing, MarksExcelFile
from exams.registration.models import ExamRegistration
from localities.models import Select2Data
from localities.serializers import Select2Serializer
from setups.academics.classes.models import SchoolClasses
from setups.academics.gradingschemes.models import GradingSchemes
from setups.academics.gradingsystem.models import GradingSystem
from setups.academics.subjects.models import Subjects
from setups.academics.termdates.models import TermDates
from setups.academics.years.models import Years
from staff.teachers.models import Teachers
from staff.teachersubjects.models import TeacherSubjects
from studentmanager.parents.models import ExcelFile
from studentmanager.student.models import Students
from studentmanager.studentsubjects.models import StudentSubjects
from useradmin.users.models import User
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)


def examprocess(request):
    return render(request,'exams/examprocessing.html')


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


def searchexamregister(request,term,year):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    terms = ExamRegistration.objects.raw(
        "SELECT top 5 exam_reg_code,exam_name FROM registration_examregistration WHERE exam_term_id = %s and exam_year_id = %s and convert(varchar(10), lock_date, 102) >= convert(varchar(10), getdate(), 102) and exam_name like %s",
        [term,year,query])

    for obj in terms:
        select2 = Select2Data()
        select2.id = str(obj.exam_reg_code)
        select2.text = obj.exam_name
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

def searchteachers(request):
    vendor=connection.vendor

    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    mysql = "SELECT teacher_code,teacher_name FROM teachers_teachers WHERE status='Active' and (teacher_name like %s or tsc_no like %s) LIMIT 5"
    mssql = "SELECT top 5 teacher_code,teacher_name FROM teachers_teachers WHERE status='Active' and (teacher_name like %s or tsc_no like %s)"
    usedquery = ''
    if (vendor == 'microsoft'):
        usedquery = mssql
    else:
        usedquery = mysql
    teachers = Teachers.objects.raw(usedquery,
       [ query,query])

    for obj in teachers:
        text = obj.teacher_name
        select2 = Select2Data()
        select2.id = str(obj.teacher_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchsubjects(request,classcode,teacher):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    classes = Subjects.objects.raw(
        # "SELECT top 5 teacher_subjectcode,subject_name FROM teachersubjects_teachersubjects"+
        # " inner join subjects_subjects  on teacher_subjectsubject_id = subject_code"+
        # " WHERE teacher_subjectclass_id = %s and teacher_subjectteacher_id = %s and subject_name like %s",
        "SELECT top 5 subject_code,subject_name from subjects_subjects where subject_code in("+
        "SELECT teacher_subjectsubject_id FROM teachersubjects_teachersubjects where teacher_subjectclass_id=%s and teacher_subjectteacher_id = %s and subject_name like %s)",
        tuple([classcode, teacher,query]))

    for obj in classes:
        text = obj.subject_name
        select2 = Select2Data()
        select2.id = str(obj.subject_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def searchstudents(request,classcode,subjects):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    students = Students.objects.raw(
        # "SELECT top 5 stud_subject_code,student_name FROM studentsubjects_studentsubjects" +
        # " inner join student_students  on stud_subject_student_id = student_code" +
        # " WHERE stud_subject_class_id = %s and stud_subject_subject_id = %s and student_name like %s",
        "SELECT top 5 student_code,adm_no,student_name from student_students where student_code in("+
        "SELECT stud_subject_student_id  from studentsubjects_studentsubjects where stud_subject_class_id = %s and stud_subject_subject_id = %s and(student_name like %s or adm_no like %s) )",
        [classcode, subjects, query,query])

    for obj in students:
        text = obj.student_name+'--'+obj.adm_no
        select2 = Select2Data()
        select2.id = str(obj.student_code)
        select2.text = text
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})


def getgradingscheme(request,id):
    response_data = {}
    exam = ExamRegistration.objects.get(pk=id)
    if exam.exam_grade_scheme is not None:
       scheme = GradingSchemes.objects.get(pk=exam.exam_grade_scheme.pk)
       response_data['gradeCode'] = scheme.scheme_code
       response_data['gradeName'] = scheme.scheme_name

       return  JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'No grading scheme set for this exam'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def processgrade(request):
    marks = request.GET.get('marks', None)
    outof = request.GET.get('outof', None)
    scheme = request.GET.get('scheme', None)

    result = float(marks)/float(outof)
    result = result * 100
    result = round(result)
    print(result)

    listsel = []
    grade= GradingSystem.objects.raw('select grading_code,grading_remarks,grading_grade from gradingsystem_gradingsystem where grading_scheme_id = %s and %s between points_from and points_to',
                                     [scheme,result])
    for obj in grade:
        response_data = {}
        response_data['grade']=obj.grading_grade
        response_data['remarks']=obj.grading_remarks
        response_data['results'] = result
        listsel.append(response_data)

    return JsonResponse(listsel,safe=False)


def saveexammarks(request):

    exam = ProcessingForm(request.POST)

    term = exam.data['exam_process_term']
    exreg = exam.data['exam_process_exam']
    classcode = exam.data['exam_process_class']
    teacher = exam.data['exam_process_teacher']
    subject = exam.data['exam_process_subject']
    student = exam.data['exam_process_student']
    year = exam.data['exam_process_year']
    user = exam.data['exam_processed_by']

    print('user :'+request.user.username)
    if term is not None and term != '':
        t = TermDates.objects.get(pk=term)
        exam.exam_process_term = t

    if exreg is not None and exreg != '':
        reg = ExamRegistration.objects.get(pk=exreg)
        exam.exam_process_exam = reg

    if classcode is not None and classcode != '':
        cl = SchoolClasses.objects.get(pk=classcode)
        exam.exam_process_class = cl

    if teacher is not None and teacher != '':
        tea = Teachers.objects.get(pk=teacher)
        exam.exam_process_teacher = tea

    if subject is not None and subject != '':
        sb = Subjects.objects.get(pk=subject)
        exam.exam_process_subject = sb

    if student is not None and student != '':
        dent = Students.objects.get(pk=student)
        exam.exam_process_student = dent

    if year is not None and year != '':
        yr = Years.objects.get(pk=year)
        exam.exam_process_year = yr

    # if user == '':
    #     u = request.user
    #     exam.exam_processed_by = u
    examex = ExamProcessing()
    try:
        examex = ExamProcessing.objects.get(exam_process_exam=exam.exam_process_exam,
                                            exam_process_subject=exam.exam_process_subject,
                                            exam_process_student=exam.exam_process_student)
    except examex.DoesNotExist:
        savedexam=exam.save()
        u = get_current_user()
        savedexam.exam_processed_by = u
        savedexam.save()

    else:
        return JsonResponse({'error': examex.exam_process_student.adm_no+' in class '+examex.exam_process_class.class_name+' already has marks for '+examex.exam_process_subject.subject_name},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JsonResponse({'success':'Marks Recorded Successfully'})


def getrecordedmarks(request):

    listsel = []

    processes = ExamProcessing.objects.raw("select top 50 exam_process_code,exam_marks,exam_outof,exam_percentage_marks,exam_process_date,exam_process_remarks,exam_processing_grade,"+
       "term_number,year_number,exam_name,class_name,student_name,adm_no,subject_name,teacher_name,username from processing_examprocessing"+
        " inner join termdates_termdates on exam_process_term_id = term_code"+
        " inner join years_years on exam_process_year_id = year_code"+
        " inner join registration_examregistration on exam_process_exam_id = exam_reg_code"+
        " inner join classes_schoolclasses on exam_process_class_id = class_code"+
        " inner join teachers_teachers on exam_process_teacher_id = teacher_code"+
        " inner join subjects_subjects on exam_process_subject_id = subject_code" +
        " inner join student_students on exam_process_student_id = student_code"+
        " inner join users_user on exam_processed_by_id = user_id")

    for obj in processes:
        response_data={}
        print(obj.student_name)
        response_data['processCode'] = obj.exam_process_code
        response_data['name'] = obj.student_name
        response_data['admNo'] = obj.adm_no
        response_data['subject'] = obj.subject_name
        response_data['teacher'] = obj.teacher_name
        response_data['term'] = obj.term_number
        response_data['marks'] = obj.exam_marks
        response_data['outof'] = obj.exam_outof
        response_data['percentage'] = obj.exam_percentage_marks
        response_data['grade'] = obj.exam_processing_grade
        response_data['remarks'] = obj.exam_process_remarks
        response_data['examDate'] = obj.exam_process_date.strftime("%Y-%m-%d")
        response_data['user'] = obj.username
        response_data['year'] = obj.year_number
        response_data['examName'] = obj.exam_name
        response_data['className'] = obj.class_name

        listsel.append(response_data)


    return JsonResponse(listsel,safe=False)

def editmarks(request,id):

    listsel = []
    processes = ExamProcessing.objects.raw(
        "select top 50 exam_process_code,exam_marks,exam_outof,exam_percentage_marks,exam_process_date,exam_process_remarks,exam_processing_grade," +
        "term_code,term_number,year_code,year_number,exam_reg_code,exam_name,class_code,class_name,student_code,student_name,adm_no,subject_code,subject_name,teacher_code,teacher_name,user_id,username from processing_examprocessing" +
        " inner join termdates_termdates on exam_process_term_id = term_code" +
        " inner join years_years on exam_process_year_id = year_code" +
        " inner join registration_examregistration on exam_process_exam_id = exam_reg_code" +
        " inner join classes_schoolclasses on exam_process_class_id = class_code" +
        " inner join teachers_teachers on exam_process_teacher_id = teacher_code" +
        " inner join subjects_subjects on exam_process_subject_id = subject_code" +
        " inner join student_students on exam_process_student_id = student_code" +
        " inner join users_user on exam_processed_by_id = user_id"+
        " where exam_process_code=%s",
        [id]
    )

    for obj in processes:
        response_data = {}
        print(obj.student_name)
        response_data['processCode'] = obj.exam_process_code
        response_data['studentCode'] = obj.student_code
        response_data['studentName'] = obj.student_name
        response_data['admNo'] = obj.adm_no
        response_data['examCode'] = obj.exam_reg_code
        response_data['examName'] = obj.exam_name
        response_data['subjectCode'] = obj.subject_code
        response_data['subjectName'] = obj.subject_name
        response_data['teacherCode'] = obj.teacher_code
        response_data['teacherName'] = obj.teacher_name
        response_data['termCode'] = obj.term_code
        response_data['termNumber'] = obj.term_number
        response_data['yearCode'] = obj.year_code
        response_data['yearNumber'] = obj.year_number
        response_data['classCode'] = obj.class_code
        response_data['className'] = obj.class_name
        response_data['marks'] = obj.exam_marks
        response_data['outof'] = obj.exam_outof
        response_data['percentage'] = obj.exam_percentage_marks
        response_data['grade'] = obj.exam_processing_grade
        response_data['remarks'] = obj.exam_process_remarks
        response_data['examDate'] = obj.exam_process_date.strftime("%Y-%m-%d")
        response_data['user'] = obj.user_id

        listsel.append(response_data)

    return JsonResponse(listsel, safe=False)


def updateexammarks(request,id):
    exam = ExamProcessing.objects.get(pk=id)

    form = ProcessingForm(request.POST, instance=exam)

    form.save()
    return JsonResponse({'success': 'Marks Updated Successfully'})

def deleteexammarks(request,id):
    exam = ExamProcessing.objects.get(pk=id)
    exam.delete()
    return JsonResponse({'success': 'Marks Deleted Successfully'})


def importmarks(request):
    if request.method == 'POST':
        file = request.FILES['file']
        obj = MarksExcelFile.objects.create(
            file=file
        )
        path = str(obj.file.path)

        print('path here...')
        print(path)
        df = pd.read_excel(path)
        print(df)
        th = df.to_dict('records')
        for obj in th:
            print(obj)
            # null=nan
            exam = ExamProcessing()
            scheme = GradingSchemes()
            if obj['EXAM'] != 'nan':
                reg = ExamRegistration()
                try:
                    reg = ExamRegistration.objects.get(exam_name=obj['EXAM'])
                    exam.exam_process_exam = reg
                    term=TermDates.objects.get(pk=reg.exam_term.pk)
                    exam.exam_process_term = term
                    year = Years.objects.get(pk=reg.exam_year.pk)
                    exam.exam_process_year=year
                    if reg.exam_grade_scheme is None:
                       return JsonResponse({'error':'Set a grade scheme for this exam'},
                                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        scheme = GradingSchemes.objects.get(pk=reg.exam_grade_scheme.pk)
                except reg.DoesNotExist:
                    return JsonResponse({'error': str(obj['EXAM']) + ' is not a valid exam'},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            if obj['CLASS'] != 'nan':
                classes = SchoolClasses()
                try:
                    classes = SchoolClasses.objects.get(class_name=obj['CLASS'])
                    exam.exam_process_class = classes
                except classes.DoesNotExist:
                    return JsonResponse({'error': str(obj['CLASS']) + ' is not a valid class'},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if obj['TEACHER'] != 'nan':
                teacher = Teachers()
                try:
                    teacher = Teachers.objects.get(staff_number=obj['TEACHER'])
                    exam.exam_process_teacher = teacher
                except teacher.DoesNotExist:
                    return JsonResponse({'error': str(obj['TEACHER']) + ' is not a valid staff number'},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            if obj['SUBJECT'] != 'nan':
                subject = Subjects()
                try:
                    subject = Subjects.objects.get(subject_name=obj['SUBJECT'])
                    exam.exam_process_subject = subject
                except subject.DoesNotExist:
                    return JsonResponse({'error': str(obj['SUBJECT']) + ' is not a valid subject'},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if obj['STUDENT'] != 'nan':
                student = Students()
                try:
                    student = Students.objects.get(adm_no=obj['STUDENT'])
                    exam.exam_process_student = student

                except student.DoesNotExist:
                    return JsonResponse({'error': str(obj['STUDENT']) + ' is not a valid adm number'},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            results = ''
            grade=''
            marks=''
            if obj['MARKS'] != 'nan':
                exam.exam_marks = obj['MARKS']
                marks=obj['MARKS']

            if obj['OUTOF'] != 'nan':
                exam.exam_outof = obj['OUTOF']
                outof=obj['OUTOF']
                result = float(marks) / float(outof)
                result = result * 100
                result = round(result)
                exam.exam_percentage_marks=result

                listsel = []
                grade = GradingSystem.objects.raw(
                    'select grading_code,grading_remarks,grading_grade from gradingsystem_gradingsystem where grading_scheme_id = %s and %s between points_from and points_to',
                    [scheme.scheme_code, result])
                for obj in grade:
                    exam.exam_processing_grade=obj.grading_grade
                    exam.exam_process_remarks = obj.grading_remarks


            examex = ExamProcessing()
            try:
               examex=ExamProcessing.objects.get(exam_process_exam=exam.exam_process_exam,exam_process_subject=exam.exam_process_subject,exam_process_student=exam.exam_process_student)
            except examex.DoesNotExist:
               exam.exam_process_date=datetime.now()
               print(request.user)
               u = User.objects.get(username=request.user)
               exam.exam_processed_by = u
               exam.save()
            else:
                return JsonResponse({
                                        'error': examex.exam_process_student.adm_no + ' in class ' + examex.exam_process_class.class_name + ' already has marks for ' + examex.exam_process_subject.subject_name},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        return JsonResponse({'success': 'Marks Imported Successfully'})


def dynamicaddress(request):
    response_data = {}
    response_data['url'] = urlsplit(
            request.build_absolute_uri(None)).scheme + '://' + request.get_host() + '/static/img/spinner.gif'
    return JsonResponse(response_data)



def get_marksData(exam,classes,teacher,subject):
    listsel = []
    processes = ExamProcessing.objects.raw(
        "select top 50 exam_process_code,display_name,exam_marks,exam_outof,exam_percentage_marks,exam_process_date,exam_process_remarks,exam_processing_grade," +
        "term_code,term_number,year_code,year_number,exam_reg_code,exam_name,class_code,class_name,student_code,student_name,adm_no,subject_code,subject_name,teacher_code,teacher_name,user_id,username from processing_examprocessing" +
        " inner join termdates_termdates on exam_process_term_id = term_code" +
        " inner join years_years on exam_process_year_id = year_code" +
        " inner join registration_examregistration on exam_process_exam_id = exam_reg_code" +
        " inner join classes_schoolclasses on exam_process_class_id = class_code" +
        " inner join teachers_teachers on exam_process_teacher_id = teacher_code" +
        " inner join subjects_subjects on exam_process_subject_id = subject_code" +
        " inner join student_students on exam_process_student_id = student_code" +
        " inner join users_user on exam_processed_by_id = user_id" +
        " where exam_process_exam_id=%s and exam_process_class_id=%s and exam_process_teacher_id=%s and exam_process_subject_id=%s",
        [exam,classes,teacher,subject]
    )

    for obj in processes:
        response_data = {}
        print(obj.student_name)
        response_data['Name'] = obj.student_name
        response_data['AdmNo'] = obj.adm_no
        response_data['Exam'] = obj.exam_name
        response_data['Display'] = obj.display_name
        response_data['Class'] = obj.class_name
        response_data['Subject'] = obj.subject_name
        response_data['Teacher'] = obj.teacher_name
        response_data['Marks'] = obj.exam_marks
        response_data['OutOf'] = obj.exam_outof
        response_data['Percentage'] = obj.exam_percentage_marks
        response_data['Grade'] = obj.exam_processing_grade
        response_data['Remarks'] = obj.exam_process_remarks
        response_data['Date'] = obj.exam_process_date.strftime("%d/%m/%Y")
        response_data['Term'] = obj.term_number
        response_data['Year'] = obj.year_number

        listsel.append(response_data)
    df = pd.DataFrame(listsel)
    print(df)
    return df


def downloadmarksexcel(request):
    exam = request.GET.get('exam', None)
    classes = request.GET.get('class', None)
    teacher = request.GET.get('teacher', None)
    subject = request.GET.get('subject', None)

    with BytesIO() as b:
        data = get_marksData(exam,classes,teacher,subject)

        with pd.ExcelWriter(b) as writer:
            data.to_excel(writer, sheet_name="Data", index=False)

        filename = f"marks.xlsx"
        res = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        res['Content-Disposition'] = f'attachment; filename={filename}'
        return res