from extras.scripts import *
# from dcim.models import Site
from netbox_netseg_automation.models import ManagementVrf, NetSegSite, SegmentVrf, HubSiteVrf
from pynetbox import api
import nbox_get_ip
NETBOX_URL = 'http://192.168.0.105:8000/'
PARENT_PREFIX_ID = 8
PREFIX_LENGTH = 29
DESCRIPTION = "vrf_xxxxx_subnet"

class NewManagementVrfScript(Script):

    class Meta:
        name = "New Vrf"
        description = "Provision a new Vrf"

    vrf_name = StringVar(
        description="Name of the new Vrf"
    )

    vpn_id = IntegerVar(
        description="VPN ID"
    ) 
    priority_one_hub_site = ObjectVar(
        model=NetSegSite,
        required=True,
        description="Select the site where the Hub VRF will be provisioned"
    )

    priority_two_hub_site = ObjectVar(
        model=NetSegSite,
        required=True,
        description="Select the site where the Hub VRF will be provisioned"
    )

    priority_three_hub_site = ObjectVar(
        model=NetSegSite,
        required=False,
        description="Select the site where the Hub VRF will be provisioned"
    )

    vrf_spoke_sites = ObjectVar(
        model=NetSegSite,
        required=False,
        description="Select the site where the Spoke VRF will be provisioned"
    )
   
    deployment_status =  StringVar(
        description="Add status"
    )

    def run(self, data, commit):
        # Access selected site
        # selected_site = data['site']

        # Create the new VRF and associate it with the selected site
        vrf = SegmentVrf.objects.create(
            name=data['vrf_name'],
            vrf_vpn_id=data['vpn_id'],
           
        )

        self.log_success(f"VRF {vrf.name} created")

        mgmt_vrf_instance =  ManagementVrf.objects.create(
            vrf_name=data['vrf_name'],
            priority_one_hub_site=data['priority_one_hub_site'],
            priority_two_hub_site=data['priority_two_hub_site'],
            priority_three_hub_site=data['priority_three_hub_site'],
            vrf_spoke_sites=data['vrf_spoke_sites'],
            deployment_status=data['deployment_status'],
           
           
        )
        self.log_success(f"new Mgmt VRF {mgmt_vrf_instance.vrf_name} instance is created")


        hub1_vrf_instance =  ManagementVrf.objects.create(
            vrf_name=mgmt_vrf_instance.vrf_name,
            hub_site=data['priority_one_hub_site'],
            vrf_to_vdom_subnet = nbox_get_ip.get_next_available_prefix(NETBOX_URL, PARENT_PREFIX_ID, PREFIX_LENGTH, DESCRIPTION),
            inter_vdom_subnet = nbox_get_ip.get_next_available_prefix(NETBOX_URL, PARENT_PREFIX_ID, PREFIX_LENGTH, DESCRIPTION),  
            vdom_loopback = nbox_get_ip.get_next_available_prefix(NETBOX_URL, PARENT_PREFIX_ID, PREFIX_LENGTH, DESCRIPTION),            
            deployment_status=data['deployment_status']
           
           
        )
        self.log_success(f"New Mgmt VRF {hub1_vrf_instance.vrf_name} is created for site - {hub1_vrf_instance.hub_site}")
