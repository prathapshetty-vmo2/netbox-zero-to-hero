from extras.reports import Report
from dcim.models import Device
from utilities.testing import TestCase

class DeviceReport(Report):
    description = "Check that all devices have a primary IP assigned"

    def test_primary_ip(self):
        for device in Device.objects.all():
            if device.primary_ip is None:
                self.info(device, f"{device.name} has no primary IP")
            else:
                self.log_success(device, f"{device.name} has a primary IP: {device.primary_ip}")
