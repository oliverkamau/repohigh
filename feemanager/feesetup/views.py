from django.shortcuts import render

# Create your views here.
def feesetupspage(request):
    return render(request,'fees/feesetups.html')
