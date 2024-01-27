# Note: for Secutiry reasons we have removed URL/endpoints to ensure safety of Database and safe-Operations 

from django.urls import path
from .views import (loginPage, logOut, registerPage,
                    homePage, sendPages, recordDetail, markStatus, widget_data_request, floatingDashboard,
                    search_clients_Stage, cidn_serviceInitiation_stage, Handle_ServiceForm,
                    search_existing_customers, register_customer,
                    download_csv, download_csv2, download_my_pdf,
                    testPage, testPage_2, run_Script, TroubleShoot,
                    detailJob,)

urlpatterns = [
    # Frequent-access
    path(, homePage, name='home-page'),
    path('', sendPages, name='requestpage'),

    # Authentication
    path('login-link', loginPage, name='login'),
    path( logOut, name='logout'),
    path( registerPage, name='register-page'),


    # Client-Service-initiation
    path(search_clients_Stage, name='create_job'),
    path(search_existing_customers, name='search-ex-cus'),
    path( cidn_serviceInitiation_stage, name='to-customer'),
    path(Handle_ServiceForm, name='ServiceFormHandler'),
    path(register_customer, name='register-customer'),

    # Service-Info_Retrieval
    path(recordDetail, name='get_record'),
    path(floatingDashboard, name='floatingDashboard'),

    # Service_State
    path( markStatus,),

    # Mixed
    path( widget_data_request, name='wdg'),

    # File_Outputs
    path( download_my_pdf, name='download_my_pdf'),
    path(download_csv, name='download_my_csv'),
    path( download_csv2, name='download_my_csv2'),

    # Testing
    path(TroubleShoot, name="troubleshoot"),
    path(testPage, name='t1'),
    path(testPage_2, name='t2'),
    path(run_Script),


]
