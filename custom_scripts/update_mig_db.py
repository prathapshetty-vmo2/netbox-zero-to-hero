import csv
import io

from extras.scripts import *
from netbox_netseg_automation.models import DeviceMigration  # Update path if needed


class ImportDeviceMigrations(Script):

    class Meta:
        name = "Import Device Migrations"
        description = "Import device migration data from CSV file"

    csv_file = FileVar(
        description="Upload CSV file with device migration data"
    )

    def run(self, data, commit):
        csv_data = data["csv_file"].read().decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(csv_data))

        created = 0
        print(reader)
        for row in reader:
            # Clean empty strings to None
            cleaned_row = {k: (v.strip() if v.strip() else None) for k, v in row.items()}
            print(cleaned_row)
            # Create and save DeviceMigration instance
            migration = DeviceMigration(
                site=cleaned_row["site"],
                pe_hostname=cleaned_row["pe_hostname"],
                vrf=cleaned_row["vrf"],
                pe_interface=cleaned_row["pe_interface"],
                ip_address=cleaned_row["ip_address"],
                dns_record=cleaned_row["dns_record"],
                mac_address=cleaned_row["mac_address"],
                sw_hostname=cleaned_row["sw_hostname"],
                sw_vlan=cleaned_row["sw_vlan"],
                sw_interface=cleaned_row["sw_interface"],
                sw_port_status=cleaned_row["sw_port_status"],
                sw_int_desc=cleaned_row["sw_int_desc"],
                tcap_ref=cleaned_row["tcap_ref"],
                migration_type=cleaned_row["migration_type"],
                mac_vendor_name=cleaned_row["mac_vendor_name"],
                tsa_vendor_vrf=cleaned_row["tsa_vendor_vrf"],
                tsa_vendor_vlan=cleaned_row["tsa_vendor_vlan"],
                new_ipaddress=cleaned_row["new_ipaddress"],
                dns_A_record_update=cleaned_row["dns_A_record_update"],
            )

            migration.save()
            created += 1
            self.log_success(f"Imported row for IP {migration.ip_address}")

        self.log_info(f"Imported {created} device migration entries.")
