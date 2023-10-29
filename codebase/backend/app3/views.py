from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from baseapp.models import CustomerRegistration
from django.http import HttpResponse


# Create your views here.
def console(request):
    return render(request, 'console/Base_console.html', )


def consoleSections(request, section=None):  # returns matching Console Sectional-Pages
    if section == 'customers':
        return CustomerDB(request)
    elif section == '':
        pass
    else:
        return HttpResponse('<div style="color:red; text-align:center;"> Request Denied!!! </div>')


# ---------------Sectional-Rendering---------------- #
def CustomerDB(request):  # Returns Entire Customers List
    return render(request, 'console/console_customers.html',
                  context={'records': CustomerRegistration.objects.all().order_by()})


# ----------------------- Actions ---------------------- #
def viewClientInfo(request, cidn=None):  # Single Client record info sent
    query = CustomerRegistration.objects.get(CustomerName=cidn)
    return render(request, 'console/partials/viewSingleClient.html', context={'data': query})

def editClientInfo(request, cidn=None):
    if request.method == 'POST':  # saving Data
        pass

    query = CustomerRegistration.objects.get(CustomerName=cidn)
    return render(request, 'console/partials/editSingleClient.html', context={'data': query})
