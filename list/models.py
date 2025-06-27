from django.db import models


class Driver(models.Model):
    name = models.CharField(max_length=100)
    truck_number = models.CharField(max_length=50)
    dims = models.CharField(max_length=100, blank=True, null=True)  # dimensions of the truck
    payload = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # max payload of the truck

    def __str__(self):
        return self.name

class Disp(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Load(models.Model):
    ref_number = models.CharField(max_length=50)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, related_name="loads")
    broker_name = models.CharField(max_length=100)
    bol = models.FileField(upload_to='bol/', blank=True, null=True) #BOL file
    rc = models.FileField(upload_to='rc/', blank=True, null=True) #RC file
    miles = models.DecimalField(max_digits=7, decimal_places=2) #total miles for the load
    disp = models.ForeignKey(Disp, on_delete=models.SET_NULL, null=True, related_name="loads")
    disp_percent = models.DecimalField("Dispatcher %", max_digits=5, decimal_places=2)
    pod = models.FileField(upload_to='pod/', blank=True, null=True)
    booked_by = models.CharField(max_length=100) #disp name
    booked_on = models.DateField()
    drivers_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.ref_number} - {self.broker_name}"