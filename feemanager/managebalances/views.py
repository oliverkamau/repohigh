from django.shortcuts import render

# Create your views here.
def balances(request):
    return render(request, 'fees/managebalances.html')
