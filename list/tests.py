from decimal import Decimal
from datetime import date
from django.test import TestCase
from list.models import Broker, Disp, Driver, Load


class LoadCalculationTests(TestCase):
    def setUp(self):
        self.broker = Broker.objects.create(name="Test Broker")
        self.disp = Disp.objects.create(name="Test Disp")

    def test_driver_payout_for_percent_driver(self):
        driver = Driver.objects.create(
            name="Percent Driver",
            pay_type=Driver.PayType.PERCENT,
            driver_percent=Decimal("30.00"),
            truck_number="#1",
        )

        load = Load.objects.create(
            ref_number="11",
            rate=Decimal("2000.00"),
            driver=driver,
            broker=self.broker,
            miles=Decimal("1000.00"),
            disp=self.disp,
            disp_percent=Decimal("3.00"),
            booked_on=date.today(),
        )

        self.assertEqual(load.driver_payout, Decimal("600.00"))

    def test_driver_payout_for_per_mile_driver_uses_minimum(self):
        driver = Driver.objects.create(
            name="Miles Driver",
            pay_type=Driver.PayType.MILES,
            driver_per_mile=Decimal("0.50"),
            truck_number="#2",
        )

        load = Load.objects.create(
            ref_number="22",
            rate=Decimal("1000.00"),
            driver=driver,
            broker=self.broker,
            miles=Decimal("100.00"),
            disp=self.disp,
            disp_percent=Decimal("3.00"),
            booked_on=date.today(),
        )

        self.assertEqual(load.driver_payout, Decimal("200.00"))

    def test_dispatcher_payout(self):
        driver = Driver.objects.create(
            name="Driver",
            pay_type=Driver.PayType.PERCENT,
            driver_percent=Decimal("25.00"),
            truck_number="#3",
        )

        load = Load.objects.create(
            ref_number="33",
            rate=Decimal("1500.00"),
            driver=driver,
            broker=self.broker,
            miles=Decimal("500.00"),
            disp=self.disp,
            disp_percent=Decimal("5.00"),
            booked_on=date.today(),
        )

        self.assertEqual(load.dispatcher_payout, Decimal("75.00"))

    def test_company_profit(self):
        driver = Driver.objects.create(
            name="driver",
            pay_type=Driver.PayType.PERCENT,
            driver_percent=Decimal("25.00"),
            truck_number="#4",
        )

        load = Load.objects.create(
            ref_number="44",
            rate=Decimal("2000.00"),
            driver=driver,
            broker=self.broker,
            miles=Decimal("1000.00"),
            disp=self.disp,
            disp_percent=Decimal("3.00"),
            booked_on=date.today(),
        )

        self.assertEqual(load.company_profit, Decimal("550.00"))
