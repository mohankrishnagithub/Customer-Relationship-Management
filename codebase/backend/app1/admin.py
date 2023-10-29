from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Job, CustomerRegistration, Warranty

# Register your models here.


admin.site.unregister(Group)  # eliminating group model


class CustomerRegAdmin(admin.ModelAdmin):
    list_display = ['id', 'CIDN', 'CustomerName', 'Created', 'Phone', 'Orders', 'EngagementTier']


class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'SIDN', 'Name', 'Model', 'Problem',  'Phone2', 'Status', 'Created', 'Updated', 'RequireUpdate']


class WarrantyAdmin(admin.ModelAdmin):
    list_display = ['id', 'Start_Date', 'End_Date', 'Description']


# Registering to AdminPanel
admin.site.register(Job, JobAdmin)
admin.site.register(CustomerRegistration, CustomerRegAdmin)
admin.site.register(Warranty, WarrantyAdmin)