from extras.scripts import *
# from dcim.models import Site
from ipam.models import Prefix
import os
import time
from netbox_netseg_automation.models import ManagementVrf, NetSegSite, SegmentVrf, HubSiteVrf, SpokeSiteVrf
from pynetbox import api
# import nbox_get_ip
NETBOX_URL = 'http://192.168.0.105:8000/'
PARENT_PREFIX_ID = 8
PREFIX_LENGTH = 29
DESCRIPTION = "vrf_xxxxx_subnet"

def get_and_create_next_prefix(prefix_id, length, description):
    """Reserve the next available prefix via pynetbox, then fetch it in the DB for ORM use."""
    netbox_token = os.getenv("NETBOX_TOKEN")
    if not netbox_token:
        raise ValueError("NETBOX_TOKEN not set")

    netbox = api(NETBOX_URL, token=netbox_token)
    parent = netbox.ipam.prefixes.get(prefix_id)
    if not parent:
        raise ValueError(f"Parent prefix ID {prefix_id} not found")

    # Reserve the next prefix (NetBox will mark it as used)
    new_api_prefix = parent.available_prefixes.create({
        "prefix_length": length,
        "description": description
    })

    # Fetch the matching prefix via ORM
    return Prefix.objects.get(prefix=new_api_prefix.prefix)



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

    vrf_spoke_sites = MultiObjectVar(
      model=NetSegSite,
      required=False,
       description="Select one or more sites where the Spoke VRF will be provisioned"
      )
   
    deployment_status =  StringVar(
        description="Add status"
    )
  

    def run(self, data, commit):
        # Access selected site
        # selected_site = data['site']

        # Create the new VRF and associate it with the selected site       
        # vrf_subnet=get_and_create_next_prefix(PARENT_PREFIX_ID, PREFIX_LENGTH, "vrf_to_vdom_subnet")      
        # vdom_subnet=get_and_create_next_prefix(PARENT_PREFIX_ID, PREFIX_LENGTH, "inter_vdom_subnet")        
        # vdom_loopback=get_and_create_next_prefix(PARENT_PREFIX_ID, PREFIX_LENGTH, "vdom_loopback")
      
        vrf = SegmentVrf.objects.create(
            name=data['vrf_name'],
            vrf_vpn_id=data['vpn_id'],
           
        )

        self.log_success(f"VRF {vrf.name} created")         
        mgmt_vrf_instance =  ManagementVrf.objects.create(
            vrf_name=vrf,
            priority_one_hub_site=data['priority_one_hub_site'],
            priority_two_hub_site=data['priority_two_hub_site'],
            priority_three_hub_site=data['priority_three_hub_site'],        
            deployment_status=data['deployment_status'],
         )
        # Now assign the many-to-many field
        if data.get('vrf_spoke_sites'):
            mgmt_vrf_instance.vrf_spoke_sites.set(data['vrf_spoke_sites'])
        
        self.log_success(f"new Mgmt VRF {mgmt_vrf_instance.vrf_name} instance is created")

        hub1_vrf_instance = HubSiteVrf.objects.create(
             vrf_name=mgmt_vrf_instance,
             hub_site=data['priority_one_hub_site'],
             vrf_to_vdom_subnet= get_and_create_next_prefix(PARENT_PREFIX_ID, PREFIX_LENGTH, "vrf_to_vdom_subnet"),
             inter_vdom_subnet=get_and_create_next_prefix(PARENT_PREFIX_ID, PREFIX_LENGTH, "inter_vdom_subnet")  ,
             vdom_loopback=get_and_create_next_prefix(PARENT_PREFIX_ID, PREFIX_LENGTH, "vdom_loopback"),
             deployment_status=data['deployment_status']
            )
           
        self.log_success(f"New Mgmt VRF {hub1_vrf_instance.vrf_name} is created for site - {hub1_vrf_instance.hub_site}")

        hub2_vrf_instance = HubSiteVrf.objects.create(
             vrf_name=mgmt_vrf_instance,
             hub_site=data['priority_two_hub_site'],
             vrf_to_vdom_subnet= get_and_create_next_prefix(PARENT_PREFIX_ID, PREFIX_LENGTH, "vrf_to_vdom_subnet"),
             inter_vdom_subnet=get_and_create_next_prefix(PARENT_PREFIX_ID, PREFIX_LENGTH, "inter_vdom_subnet")  ,
             vdom_loopback=get_and_create_next_prefix(PARENT_PREFIX_ID, PREFIX_LENGTH, "vdom_loopback"),
             deployment_status=data['deployment_status']
            )
           
        self.log_success(f"New Mgmt VRF {hub2_vrf_instance.vrf_name} is created for site - {hub2_vrf_instance.hub_site}")

        if data.get('priority_three_hub_site'):
            hub3_vrf_instance = HubSiteVrf.objects.create(
             vrf_name=mgmt_vrf_instance,
             hub_site=data['priority_three_hub_site'],
             vrf_to_vdom_subnet= get_and_create_next_prefix(PARENT_PREFIX_ID, PREFIX_LENGTH, "vrf_to_vdom_subnet"),
             inter_vdom_subnet=get_and_create_next_prefix(PARENT_PREFIX_ID, PREFIX_LENGTH, "inter_vdom_subnet")  ,
             vdom_loopback=get_and_create_next_prefix(PARENT_PREFIX_ID, PREFIX_LENGTH, "vdom_loopback"),
             deployment_status=data['deployment_status']
            )
           
            self.log_success(f"New Mgmt VRF {hub3_vrf_instance.vrf_name} is created for site - {hub3_vrf_instance.hub_site}")

        if data.get('vrf_spoke_sites'):        
           for spoke_vrf in data['vrf_spoke_sites']:
              spoke_vrf_inst = SpokeSiteVrf.objects.create(
                  name = spoke_vrf,
                  mgmt_vrf=mgmt_vrf_instance,
                  spoke_targets=[],
                  build_status =data['deployment_status']
 
                 )
              self.log_success(f"New Mgmt VRF {spoke_vrf_inst.name} is created for site - {spoke_vrf.name}")                                                      
