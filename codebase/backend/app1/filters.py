import django_filters
from django_filters import DateFilter
from .models import Job

class CustomerFilter(django_filters.FilterSet):
    Phone2 = django_filters.NumberFilter(lookup_expr='icontains', label='alt-phone')
    Name__Phone = django_filters.NumberFilter(lookup_expr='icontains', label='phone')
    Name__CustomerName = django_filters.CharFilter(lookup_expr='icontains', label='Name')
    Created = django_filters.DateRangeFilter(label='select')
    start_date = DateFilter(field_name='Created', lookup_expr='gte', label='start')
    end_date = DateFilter(field_name='Created', lookup_expr='lte', label='end')

    class Meta:
        model = Job
        fields = {
                  'Status': ['exact'],
                  'Model': ['icontains'],
                  'Type': ['exact'],
                  'id': ['exact'],
                  'Payment': ['exact'],



                   }
