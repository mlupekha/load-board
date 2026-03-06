from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


class Driver(models.Model):
    class PayType(models.TextChoices):
        PERCENT = "percent_of_gross", "Percent of gross"
        MILES = "per_mile", "Per mile"

    name = models.CharField(max_length=100)

    pay_type = models.CharField(
        max_length=20,
        choices=PayType.choices,
        default=PayType.PERCENT,
    )

    driver_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Percent of gross (30.00 means 30%)",
    )
    driver_per_mile = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Amount per mile (0.50 means $0.5 per mile)",
    )
    truck_number = models.CharField(max_length=50)
    dims = models.CharField(max_length=100, blank=True, null=True)
    payload = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.truck_number}"

class Disp(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Broker(models.Model):
    name = models.CharField(max_length=100, unique=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Load(models.Model):
    ref_number = models.CharField(max_length=50)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, related_name="loads")
    broker = models.ForeignKey(Broker, on_delete=models.SET_NULL, null=True, related_name="loads")
    bol = models.FileField(upload_to='bol/', blank=True, null=True) #BOL file
    rc = models.FileField(upload_to='rc/', blank=True, null=True) #RC file
    miles = models.DecimalField(max_digits=7, decimal_places=2) #total miles for the load
    disp = models.ForeignKey(Disp, on_delete=models.SET_NULL, null=True, related_name="loads")
    #disp % variants with 3% as default
    disp_percent = models.DecimalField(
        "Dispatcher %",
        max_digits=5,
        decimal_places=2,
        choices=[
            (Decimal("1.00"), "1%"),
            (Decimal("2.00"), "2%"),
            (Decimal("3.00"), "3%"),
            (Decimal("5.00"), "5%"),
        ], default=Decimal("3.00"),
    )
    pod = models.FileField(upload_to='pod/', blank=True, null=True)
    booked_on = models.DateField()
    drivers_payout_final = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dispatcher_payout_final = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    company_profit_final = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)



    def __str__(self):
        broker_name = self.broker.name if self.broker else "No Broker"
        return f"{self.ref_number} - {broker_name}"


    @staticmethod
    def _quantize(amount: Decimal) -> Decimal:
        return amount.quantize(Decimal("0.01"), rounding="ROUND_HALF_UP")

    #function to calculate the payouts for different pay types
    @property
    def driver_payout(self) -> Decimal:
        if not self.driver:
            return Decimal("0.00")
        if self.driver.pay_type == Driver.PayType.PERCENT:
            percent = Decimal(self.driver.driver_percent or 0) / Decimal("100")
            payout = Decimal(self.rate or 0) * percent
            return self._quantize(payout)
        per_mile = Decimal(self.driver.driver_per_mile or 0)
        miles = Decimal(self.miles or 0)
        payout = per_mile * miles
        payout = max(payout, Decimal("200.00"))
        return self._quantize(payout)

    @property
    def dispatcher_payout(self) -> Decimal:
        percent = Decimal(self.disp_percent or 0) / Decimal("100")
        payout = Decimal(self.rate or 0) * percent
        return self._quantize(payout)

    @property
    def company_profit(self) -> Decimal:
        miles_cost = Decimal(self.miles or 0) * Decimal("1.45")
        profit = Decimal(self.rate or 0) - miles_cost
        return self._quantize(profit)

    def clean(self):
        if self.rate is not None and self.rate < 0:
            raise ValidationError("Rate cannot be negative")
        if self.miles is not None and self.miles < 0:
            raise ValidationError("Miles cannot be negative")
        if self.driver:
            if self.driver.pay_type == Driver.PayType.PERCENT and not self.driver.driver_percent:
                raise ValidationError({"driver": "Driver percent must be set for percent pay type"})
            if self.driver.pay_type == Driver.PayType.MILES and not self.driver.driver_per_mile:
                raise ValidationError({"driver": "Driver per mile must be set for per mile pay type"})


    def save(self, *args, **kwargs):
        # if the field is empty, set it to the calculated value, you can also set it manually if needed
        if self.drivers_payout_final is None:
            self.drivers_payout_final = self.driver_payout
            
        if self.dispatcher_payout_final is None:
            self.dispatcher_payout_final = self.dispatcher_payout
            
        if self.company_profit_final is None:
            self.company_profit_final = self.company_profit
            
        super().save(*args, **kwargs)
