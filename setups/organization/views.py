from urllib.parse import urlsplit

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from setups.organization.forms import OrganizationForm
from setups.organization.models import Organization


def getorgpage(request):
    return render(request,'setups/organization/organization.html')


def createorganization(request):
    org = OrganizationForm(request.POST, request.FILES)
    orgs=Organization.objects.all()
    if orgs:
      for o in orgs:
         o.delete()

    org.save()

    return JsonResponse({'success': 'Organization Saved Successfully!'})


def updateorganization(request,id):
    org = Organization.objects.get(pk=id)

    form = OrganizationForm(request.POST, request.FILES, instance=org)

    form.save()
    return JsonResponse({'success': 'Organization Updated Successfully'})

def editorganization(request,id):
    response_data = {}
    org = Organization.objects.get(pk=id)
    response_data['code'] = org.organization_code
    response_data['name'] = org.organization_name
    response_data['address'] = org.physical_address
    response_data['postal'] = org.postal_address
    response_data['telno'] = org.organization_telno
    response_data['cellno'] = org.organization_cellno
    response_data['websites'] = org.organization_websites
    response_data['email'] = org.organization_email
    response_data['mission'] = org.organization_mission
    response_data['vision'] = org.organization_vision
    response_data['motto'] = org.organization_motto

    if org.organization_logo:
        response_data['url'] = urlsplit(
            request.build_absolute_uri(None)).scheme + '://' + request.get_host() + org.organization_logo.url

    return JsonResponse(response_data)


def getorganizations(request):
   listsel = []
   orgs = Organization.objects.all()
   for org in orgs:
     response_data = {}
     response_data['code'] = org.organization_code
     response_data['name'] = org.organization_name
     response_data['telno'] = org.organization_telno
     response_data['cellno'] = org.organization_cellno
     response_data['email'] = org.organization_email
     response_data['websites'] = org.organization_websites
     listsel.append(response_data)

   return JsonResponse(listsel,safe=False)

def deleteorganization(request,id):
    org = Organization.objects.get(pk=id)
    org.delete()
    return JsonResponse({'success':'Organization Deleted Successfully'})