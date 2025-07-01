from extras.scripts import *
from dcim.models import Site
from netbox_netseg_automation.models import SegmentVrf

class NewSegmentVrfScript(Script):

    class Meta:
        name = "New Vrf"
        description = "Provision a new Vrf"

    site = ObjectVar(
        model=Site,
        required=True,
        description="Select the site where the VRF will be provisioned"
    )

    vrf_name = StringVar(
        description="Name of the new Vrf"
    )

    vpn_id = IntegerVar(
        description="VPN ID"
    )

    def run(self, data, commit):
        # Access selected site
        selected_site = data['site']

        # Create the new VRF and associate it with the selected site
        vrf = SegmentVrf.objects.create(
            name=data['vrf_name'],
            vrf_vpn_id=data['vpn_id'],
            site=selected_site  # Assuming SegmentVrf has a ForeignKey to Site
        )

        self.log_success(f"VRF {vrf.name} created for site {selected_site.name}")
