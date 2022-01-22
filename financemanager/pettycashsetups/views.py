from django.shortcuts import render

# Create your views here.
def pettypage(request):
    return render(request,'finance/pettycashsetups.html')