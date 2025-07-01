from extras.scripts import *
from django.utils.text import slugify

from dcim.choices import DeviceStatusChoices, SiteStatusChoices
from dcim.models import Device, DeviceRole, DeviceType, Site
from netbox_netseg_automation.models import SegmentVrf

class NewSegmentVrfScript(Script):

    class Meta:
        name = "New Vrf"
        description = "Provision a new Vrf"

    vrf_name = StringVar(
        description="Name of the new Vrf"
     )
    vpn_id = IntegerVar(
        description="VPN ID"
     )
    # bgp_as =IntegerVar(
    #     description="BGP AS"
    #  )
   
    def run(self, data, commit):

        # Create the new site
        vrf = SegmentVrf(
            name=data['vrf_name'],
            vrf_vpn_id=data['vpn_id']
           
           
        )
        vrf.save()
        self.log_success(f"Created new vrf: {vrf}")

        # # Create access switches
        # switch_role = DeviceRole.objects.get(name='Access Switch')
        # for i in range(1, data['switch_count'] + 1):
        #     switch = Device(
        #         device_type=data['switch_model'],
        #         name=f'{site.slug.upper()}-SW-{i}',
        #         site=site,
        #         status=DeviceStatusChoices.STATUS_PLANNED,
        #         role=switch_role
        #     )
        #     switch.save()
        #     self.log_success(f"Created new switch: {switch}")

      

     
