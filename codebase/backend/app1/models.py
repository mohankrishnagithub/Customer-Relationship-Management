from django.db import models


# Create your models here.

Status_choices = (('pending', 'pending'), ('Ready', 'Ready'), ('Failed', 'Failed'),
                  ('Delivered', 'Delivered'), ('Returned', 'Returned'),)   # modelValue, userReadableValue
Type_choices = (('adapter', 'adapter'), ('mobile', 'mobile'), ('printer', 'printer'), ('tablet', 'tablet'),
                ('smps', 'smps'), ('ups', 'ups'), ('motherboard', 'motherboard'), ('monitor', 'monitor'),
                ('laptop', 'laptop'), ('desktop', 'desktop'), ('screen', 'screen'), ('audio', 'audio'), ('?', '?'),)
payment_choices = (('Pending', 'Pending'), ('Paid', 'Paid'), ('N/A', 'N/A'))
Engagement_status = (('NA', 'Not Assigned'), ('Elite', 'Elite'), ('Regular', 'Regular'), ('Basic', 'Basic'), ('Caution', 'Caution'))


class CustomerRegistration(models.Model):
    # CIDN  (client-identification)
    id = models.SmallIntegerField()
    CIDN = models.IntegerField(primary_key=True)
    CustomerName = models.CharField(max_length=40)
    Phone = models.PositiveIntegerField(null=True)
    Orders = models.PositiveIntegerField(default=0)
    Created = models.DateTimeField(null=True, auto_now_add=True)
    EngagementTier = models.CharField(max_length=10, default='NA', choices=Engagement_status, blank=True)

    def __str__(self):
        return self.CustomerName


class Job(models.Model):
    # SIDN (service-identification)
    id = models.SmallIntegerField()
    SIDN = models.IntegerField(primary_key=True)
    Name = models.ForeignKey(CustomerRegistration, on_delete=models.CASCADE)
    Problem = models.CharField(max_length=30,  null=True, blank=True, default='empty')
    Status = models.CharField(max_length=10, choices=Status_choices, default="pending")
    Payment = models.CharField(max_length=7, choices=payment_choices, default='unpaid')
    Type = models.CharField(max_length=15, choices=Type_choices, default='?')
    Model = models.CharField(max_length=15, null=True)
    Price = models.IntegerField(null=True, blank=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    Description = models.TextField(null=True, blank=True)
    Phone2 = models.PositiveIntegerField(blank=True, null=True)
    RequireUpdate = models.BooleanField(default=False)
    SN = models.CharField(max_length=15, null=True, blank=True)

class Warranty(models.Model):
    Start_Date = models.DateTimeField()
    End_Date = models.DateTimeField()
    Description = models.TextField()

