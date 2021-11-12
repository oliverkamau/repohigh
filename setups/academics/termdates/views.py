import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_control

from setups.academics.classes.models import SchoolClasses
from setups.academics.termdates.forms import TermForm
from setups.academics.termdates.models import TermDates
from localities.models import Select2Data
from localities.serializers import Select2Serializer

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def termdates(request):
    return render(request, 'setups/academics/termdates.html')


def createtermdates(request):
    current=''
    if request.method == 'POST' and 'current_term' in request.POST:
        val = request.POST['current_term']
        current = val
    else:
        current = ''
    term = TermForm(request.POST)
    cl = term.data['term_class']
    # from_date = term.data['from_date']
    # to_date = term.data['to_date']

    # date_from=datetime.datetime.strptime(from_date, "%Y-%m-%d").date();
    # date_to=datetime.datetime.strptime(to_date, "%Y-%m-%d").date();
    # term.from_date=date_from
    # term.to_date=date_to
    if cl is not None and cl != '':
        termClass = SchoolClasses.objects.get(pk=cl)
        term.term_class = termClass

    if current is not None and current == 'on':
        term.current_term = True
    else:
        term.current_term = False

    term.save()
    return JsonResponse({'success': 'Term Saved Successfully'})


def gettermdates(request):
    listsel = []
    terms = TermDates.objects.raw(
        "SELECT DISTINCT t.term_code,t.term_number,t.current_term,t.from_date,t.to_date,s.class_name FROM termdates_termdates t" +
        " LEFT JOIN classes_schoolclasses s ON t.term_class_id =s.class_code")

    for obj in terms:
        if obj.term_code not in listsel:
            response_data = {}
            response_data['termCode'] = obj.term_code
            if obj.class_name is None:
                response_data['className'] = "Not Set"
            else:
                response_data['className'] = obj.class_name
            response_data['currentTerm'] = obj.current_term
            response_data['fromDate'] = obj.from_date.strftime("%d/%m/%Y")
            response_data['toDate'] = obj.to_date.strftime("%d/%m/%Y")
            response_data['termNumber'] = obj.term_number

            listsel.append(response_data)

    return JsonResponse(listsel, safe=False)


def edittermdates(request,id):
    terms = TermDates.objects.get(pk=id)
    response_data = {}
    if terms.term_class is not None:
        termClass = SchoolClasses.objects.get(pk=terms.term_class.pk)
        response_data['classCode'] = termClass.class_code
        response_data['className'] = termClass.class_name
    response_data['termNumber'] = terms.term_number
    response_data['termCode'] = terms.term_code
    response_data['fromDate'] = terms.from_date.strftime("%Y-%m-%d")
    response_data['toDate'] = terms.to_date.strftime("%Y-%m-%d")
    response_data['currentTerm'] = terms.current_term
    return JsonResponse(response_data)


def updatetermdates(request,id):
    terms = TermDates.objects.get(pk=id)
    form = TermForm(request.POST, instance=terms)
    form.save()
    return JsonResponse({'success': 'Term Updated Successfully'})


def deletetermdates(request,id):
    terms = TermDates.objects.get(pk=id)
    terms.delete()
    return JsonResponse({'success': 'Term Deleted Successfully'})


def searchclasses(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        query = '%' + query + '%'
    else:
        query = '%' + '' + '%'

    listsel = []
    classes = SchoolClasses.objects.raw(
        "SELECT top 5 class_code,class_name FROM classes_schoolclasses WHERE classes_schoolclasses.class_name like %s or classes_schoolclasses.form like %s",
        tuple([query, query]))

    for obj in classes:
        select2 = Select2Data()
        select2.id = str(obj.class_code)
        select2.text = obj.class_name
        serializer = Select2Serializer(select2)

        listsel.append(serializer.data)

    return JsonResponse({'results': listsel})