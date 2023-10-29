from django.shortcuts import render, HttpResponse
from baseapp.models import Job
from sendresponse.models import Response

# Create your views here.
def loadPage(request):
    return render(request, 'sendresponse/index.html')

def validateRespond(request):
    x, y = request.POST['c_id'], request.POST['cell']
    print('received', x, y)
    valid_credentials = Job.objects.filter(id=x, Name__Phone=y).exists()

    if valid_credentials:
        query = Response.objects.filter(Case_id=x).order_by('-Added')
        record = Job.objects.get(id=x, Name__Phone=y)
        return render(request, 'sendresponse/partials/lists.html',
                      context={'statuses': query, 'enable_button': record.RequireUpdate, 'x': x, 'y': y, 'z': record.Status})
    else:
        return HttpResponse("Record doesn't exist")


def mark_update_required(request, case_id, phn):
    valid_credentials = Job.objects.filter(id=case_id, Name__Phone=phn).exists()

    if valid_credentials:
        print('entered')
        query = Job.objects.get(id=case_id, Name__Phone=phn)
        query.RequireUpdate = True
        query.save()
    else:
        print("didn't validate")

    return HttpResponse('<p style="color: red; text-align: center;">please wait for the store to update status</p>')





