import os
from pynetbox import api

def get_next_available_prefix(netbox_url, parent_prefix_id, prefix_length, description=None):
    """
    Get the next available prefix from a parent prefix in NetBox.

    Args:
        netbox_url (str): The NetBox API URL.
        parent_prefix_id (int): The ID of the parent prefix.
        prefix_length (int): The desired prefix length (e.g., 29).
        description (str, optional): Description for the new prefix.

    Returns:
        dict: Details of the newly created prefix, or None if failed.
    """
    try:
        netbox_token = os.getenv("NETBOX_TOKEN")
        if not netbox_token:
            print("NETBOX_TOKEN environment variable is not set.")
            return None

        # Connect to NetBox
        netbox = api(netbox_url, token=netbox_token)

        # Get the parent prefix
        prefix = netbox.ipam.prefixes.get(parent_prefix_id)
        if not prefix:
            print(f"Parent prefix with ID {parent_prefix_id} not found.")
            return None

        # Create the next available prefix
        new_prefix = prefix.available_prefixes.create({
            "prefix_length": prefix_length,
            "description": description or "auto-assigned"
        })

        return new_prefix

    except Exception as e:
        print(f"Error while retrieving/creating prefix: {e}")
        return None


# Example usage:
if __name__ == "__main__":
    NETBOX_URL = 'http://192.168.0.105:8000/'
    PARENT_PREFIX_ID = 8
    PREFIX_LENGTH = 29
    DESCRIPTION = "vrf_cisco_tni_subnet"

    result = get_next_available_prefix(NETBOX_URL, PARENT_PREFIX_ID, PREFIX_LENGTH, DESCRIPTION)
    if result:
        print("New prefix assigned:", result)
