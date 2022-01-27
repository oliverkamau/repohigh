from django.http import JsonResponse

from schoolsys.settings import SESSION_EXPIRE_SECONDS


def custom404(request, exception=None):
    return JsonResponse({
        'status_code': 404,
        'error': 'The resource was not found'
    })


def getrefreshtime(request):
    response_data = {}
    response_data['session']=SESSION_EXPIRE_SECONDS
    return JsonResponse(response_data)