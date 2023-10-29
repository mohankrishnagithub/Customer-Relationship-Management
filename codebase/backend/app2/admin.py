from django.contrib import admin
from .models import Response

# Register your models here.
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'Case_id', 'Message', 'Added']


admin.site.register(Response, ResponseAdmin)

