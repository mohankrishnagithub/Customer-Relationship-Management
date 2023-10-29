from django.shortcuts import render, redirect, reverse
from .models import Job, CustomerRegistration
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import HttpResponse
from .filters import CustomerFilter
from .form import CustomerForm, FilterForm
from datetime import datetime
from sendresponse.models import Response
from django.template.loader import get_template, render_to_string
from weasyprint import HTML, CSS
import csv, random
import pandas as pd


# Create your views here.
customers_queryset_cache = CustomerRegistration.objects.all()
jobs_queryset_cache = Job.objects.all().order_by('-Updated', '-id', )
pgn_jobs_cache = Paginator(jobs_queryset_cache, 15)


def loginPage(request):
    if request.method == 'POST':
        user_validated = authenticate(username=request.POST['user-name'], password=request.POST['pass-word'])
        if user_validated:
            login(request, user_validated)
            return redirect('home-page')
        else:
            return HttpResponse('Wrong User Credentials')

    return render(request, 'baseapp/loginForm.html')


def logOut(request):
    logout(request)
    return redirect("home-page")


def registerPage(request):
    return render(request, 'baseapp/registerForm.html')


@login_required
def homePage(request, internal_invoke_id=None):
    global_queryset = jobs_queryset_cache
    data_to_dash = global_queryset.filter(id=internal_invoke_id)[0] if internal_invoke_id else None

    djfilter = CustomerFilter(request.POST, queryset=global_queryset)  # O-0-0-0

    db_count, db_process = customers_queryset_cache.count(), global_queryset.filter(Status='pending').count()
    db_completed, db_atStore = global_queryset.filter(Status='Ready').count(), global_queryset.exclude(Status__in=['Delivered', 'Returned']).count()

    context = {'rows': None, 'db_count': db_count, 'db_atStore': db_atStore, 'db_today': today_new_entries(),
               'form': djfilter.form, 'db_process': db_process, 'db_completed': db_completed, 'data': data_to_dash,}

    if request.POST.get('djf', False):
        context['rows'] = djfilter.qs
        context['djf'] = True
    else:
        context['rows'] = pgn_jobs_cache.page(1)

    return render(request, 'baseapp/index.html', context=context)

@csrf_exempt
def sendPages(request, pg):
    print('page request occured', pg)

    if pgn_jobs_cache.num_pages < pg:
        return HttpResponse('<tr><td colspan="11" style="color:red"> End of the Records </td></tr>')

    return render(request, 'baseapp/partials/hmpgTableRenderHTMX.html', context={'page':pg+1, 'rows':pgn_jobs_cache.page(pg)})


@csrf_exempt
def recordDetail(request, ID=None):  # data to Dashboard
    user_obj = Job.objects.filter(id=ID)
    context = None

    if user_obj:
        context = {'data': user_obj[0]}
    else:
        print('empty query', id)

    return render(request, 'baseapp/dashboard.html', context=context)

@csrf_exempt
def detailJob(request, ID):  # This is unused as this will be replaced by wide dashboard
    query = jobs_queryset_cache.get(id=ID)
    context = {'data': query, 'older': get_diff(query.Created), 'hours': get_diff(query.Created, hour=True)}
    return render(request, 'baseapp/detailjob.html', context=context)

# ------------------------------------------------------------------------------------------
def search_clients_Stage(request):  # returns a page to add customers
    x = Job.objects.all().order_by('-Created')[:3]  # recent 3 Clients
    return render(request, 'baseapp/addJob.html', context={'recent_items': x})

@csrf_exempt
def search_existing_customers(request):  # returns matching registered customers records
    user_input = request.POST.get('searchBox').split()
    filtered_qs = None
    if not user_input:
        pass  # user has nothing in searchBox
    else:
        filtered_qs = CustomerRegistration.objects.filter(CustomerName__icontains=user_input[0]) | \
                      CustomerRegistration.objects.filter(
                          Phone__icontains=user_input[1] if len(user_input) > 1 else 'zzz') | \
                      CustomerRegistration.objects.filter(Phone__icontains=user_input[0])

    context = {'foundUsers': filtered_qs}
    return render(request, 'baseapp/partials/found-results.html', context=context)


def cidn_serviceInitiation_stage(request, cidn):  # to send page to add jobs to customer after choosing customer
    context = {'user_obj': CustomerRegistration.objects.get(CIDN=int(cidn))}
    return render(request, 'baseapp/jobToCustomer.html', context=context)

@csrf_exempt
def Handle_ServiceForm(request, fcidn=None):
    if request.method == 'GET':  # returns an Empty Form
        context = {'cidn': fcidn}
        return render(request, 'baseapp/partials/tiny_job_form.html', context=context)

    # Let's Register Service to System
    parent_obj = CustomerRegistration.objects.get(CIDN=fcidn)
    nums = get_new_sidn_id()
    payload = Job(id = nums[0],
                  SIDN = nums[1],
                  Name=parent_obj,
                  Type=request.POST['Type'],
                  Model=request.POST['Model'],
                  SN=request.POST['SN'],
                  Problem=request.POST['Problem'],
                  Price=request.POST['Price'],
                  Phone2=request.POST['Phone2'],
                  Payment=request.POST['Payment'],
                  Description=request.POST['Description'],)

    payload.save()
    print('Form Saved!!!')

    ''' 
    global pgn_jobs_cache
    pgn_jobs_cache = Paginator(jobs_queryset_cache, 15)
    # Updating paginator if a record is missing'''

    return HttpResponse('Reload!!!')


@csrf_exempt
def register_customer(request): # new customer registering to database
    name, phone = request.POST['name'], request.POST['phone']

    if len(phone) > 10 or len(phone) < 10:
        return HttpResponse('<p id="error_input">Invalid phone Number</p>')

    nums = get_new_cidn_id()
    creating_user = CustomerRegistration(id=nums[0], CIDN=nums[1],
                                         CustomerName=name, Phone=phone)
    creating_user.save()
    return HttpResponse('<p id="success_input">successfully Registered!</p>')

@csrf_exempt
def markStatus(request, action=None, sidn=None):
    instance = Job.objects.get(SIDN=sidn)
    if action == 'ready':
        instance.Status = 'Ready'
        instance.RequireUpdate = False
        instance.save()
        response_model('Ready for Pick up', sidn)
        return render(request, 'baseapp/snippets/postReadyNowDeliverable.html')
    elif action == 'failed':
        instance.Status = 'Failed'
        instance.RequireUpdate = False
        instance.save()
        response_model('Service Unsuccessful', sidn)
        return render(request, 'baseapp/snippets/postFailedNowReturnable.html')
    elif action == 'delivered':
        instance.Status = 'Delivered'
        instance.RequireUpdate = False
        instance.save()
        response_model('Service Concluded', sidn)
        return render(request, 'baseapp/snippets/stateComplete.html')
    elif action == 'returned':
        instance.Status = 'Returned'
        instance.RequireUpdate = False
        instance.save()
        response_model('Return Completed', sidn)
        return render(request, 'baseapp/snippets/stateReturned.html')
    else:
        return HttpResponse('Invalid Response!!!')


def widget_data_request(request, category):
    print(category)

    if category == 1:
        query = Job.objects.filter(Status='pending')
        return render(request, 'baseapp/partials/widgetSimpleRender.html', context={'rows': query})
    elif category == 2:
        query = Job.objects.filter(Status='Ready')
        return render(request, 'baseapp/partials/widgetSimpleRender.html', context={'rows': query})
    elif category == 3:
        date = datetime.strftime(datetime.now(), '%Y-%m-%d')
        query = jobs_queryset_cache.filter(Created__icontains=date)
        return render(request, 'baseapp/partials/widgetSimpleRender.html', context={'rows': query})
    else:
        return HttpResponse('Invalid request !!!')


def floatingDashboard(request, ID=None):
    return render(request, 'baseapp/floatingDashboard.html', context={})


def today_new_entries():
    date = datetime.strftime(datetime.now(), '%Y-%m-%d')
    x = jobs_queryset_cache.filter(Created__icontains=date)
    return x.count()


def download_my_pdf(request):
    my_context = {'items': ['hare', 'krishna', 'hare', 'hare']}

    my_template = get_template('baseapp/test.html').render(context=my_context)
    pdf_file = HTML(string=my_template).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')  # content_type='application/pdf'
    response['Content-Disposition'] = 'filename="home_page.pdf"'

    return response


def download_csv(request):
    response = HttpResponse(content_type="text/csv",
                            headers={"Content-Disposition":'attachment; filename="yourSeaYesWee.csv"'})

    writer = csv.writer(response)
    # writer.writerow(['first row', 'Foo', 'Bar', 'Baz'])
    # writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
    writer.writerow(['ID', 'Name', 'Problem', 'Status', 'Payment',
                     'Type', 'Model', 'Price', 'Created', 'Updated',
                     'Description', 'Phone2', 'RequireUpdate', 'SN'])

    query = Job.objects.all()
    for item in query:
        data = [item.id, item.Name, item.Problem, item.Status, item.Payment,
                item.Type, item.Model, item.Price,
                item.Created.strftime("%Y-%m-%d %H:%M:%S.%f"), item.Updated.strftime("%Y-%m-%d %H:%M:%S.%f"),
                item.Description, item.Phone2, item.RequireUpdate, item.SN]

        writer.writerow(data)

    return response


def download_csv2(request):
    response = HttpResponse(content_type="text/csv",
                            headers={"Content-Disposition":'attachment; filename="CustomerRegistrationNew.csv"'})

    writer = csv.writer(response)
    writer.writerow(['CustomerName', 'Phone', 'Orders', 'Created', 'EngagementTier'])

    query, count = CustomerRegistration.objects.all(), 0
    for item in query:
        data = [item.CustomerName, item.Phone, item.Orders,
                item.Created.strftime("%Y-%m-%d 10:58:40.%f"), item.EngagementTier]

        writer.writerow(data)
        count += 1

    print('Wrote', count, 'records')
    return response


def get_new_cidn_id():
    query = CustomerRegistration.objects.last()
    # if not query:return 1000157 'This line is for Empty Database'

    grab_seconds = datetime.now().strftime('%S')
    generated_sequence = [query.id+1, int(str(query.CIDN+100)[:5] + grab_seconds)]
    return generated_sequence

def get_new_sidn_id():
    query = Job.objects.last()
    # if not query:return 1000157 'This line is for Empty Database'

    grab_seconds = datetime.now().strftime('%S')
    generated_sequence = [query.id+1, int(str(query.SIDN+100)[:5] + grab_seconds)]
    return generated_sequence


def response_model(message, sidn):
    query = Response(Case_id=sidn, Message=message)


# ----------------------------------------------------------------------------------------------------------------------
def run_Script(request):
    # Load scripts Here
    print('Action reached!!!')
    return HttpResponse('Script Ran Succesfully !!!')


@csrf_exempt
def testPage(request):
    my_context = {'items': ['Lenovo g560', 'Microtek-ups', 'Samsung G7 monitor', 'Hare-Krishna']}
    return render(request, 'baseapp/test.html', context=my_context)


def testPage_2(request):
    return render(request, 'baseapp/test2.html', context={})


def TroubleShoot(request):
    # Empty Job
    return HttpResponse("Troubleshooter empty!")


