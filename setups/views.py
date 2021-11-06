from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def academics(request):
    return render(request, 'setups/academics/academic_setup.html')