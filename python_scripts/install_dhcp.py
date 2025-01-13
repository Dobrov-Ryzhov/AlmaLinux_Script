import os

def greeting():
    
    # Installing and configuring a DHCP Server
    def install_dhcp():
        
        os.system('sudo dnf -y install dhcp-server')
        print('The DHCP server is installed on your server\n')
        yesorno = None
        no_list = ('NO', 'No', 'no', 'N', 'n')
        yes_list = ('YES', 'Yes', 'yes', 'Y', 'y')
        while True:            
            # Config DHCP Server
            def config_dhcp():
                os.system('ip -br link show')
                subnet = input('Subnet: ')
                netmask = input('Netmask: ')
                in_range = input('Initial ip address: ')
                des_range = input('Destination ip address: ')
                route = input('Routers: ')
                domain_name = input('Domain-name: ')
                domain_name_server = input('Domain-name-server: ')
                net_card = input('Your network card is looking inside the network: ')

                config_content_dhcp = f"""
subnet {subnet} netmask {netmask} {{
    interface {net_card};
    range {in_range} {des_range};
    option domain-name-servers {domain_name_server};
    option domain-name "{domain_name}";
    option routers {route};
    option broadcast-address {subnet[:-1] + "255"};
    default-lease-time 600;
    max-lease-time 7200;
}}
"""
                os.system('sudo rm /etc/dhcp/dhcpd.conf')
                print('Creating a new configuration file')
                os.system('sudo touch /etc/dhcp/dhcpd.conf')
                
                try:
                    with open('/etc/dhcp/dhcpd.conf', 'w') as file:
                        file.write(config_content_dhcp)
                except OSError as e:
                    print(f"Error writing to dhcpd.conf: {e}")

                startup_yes = ('YES', 'Yes', 'yes', 'Y', 'y')
                startup_no = ('NO', 'No', 'no', 'N', 'n')
                startup = input('Add to auto-upload? (yes or no): ')
                if startup in startup_yes:
                    os.system('sudo systemctl enable dhcpd')
                runs = input('Start the DHCP server? (yes or no): ')
                if runs in startup_yes:
                    os.system('sudo systemctl start dhcpd')
                addfirewald = input('Add rules to firewalld? (yes or no):')
                if addfirewald in startup_yes:
                    os.system('sudo firewall-cmd --permanent --add-service=dhcp')
                    os.system('sudo firewall-cmd --reload')
                
                print('Configuration file setup was completed successfully \n')
            
            yesorno = input('Configure the DHCP server? (yes or no): ')
            if yesorno in yes_list:
                config_dhcp()
                break
            elif yesorno in no_list:
                print('You can later turn to automatic script configuration or manually correct the config located in /etc/dhcp/dhcpd.conf.\n')
                break
            
    # Removing the DHCP Server
    def removing_dhcp():
        print('Remove DHCP-Server')
        os.system('sudo dnf -y remove dhcp-server')
        print('Done\n')
        print('Remove folder /etc/dhcp')
        os.system('sudo rm -r /etc/dhcp')
        print('Done\n')
        print('Remove rules firewalld')
        os.system('sudo firewall-cmd --permanent --remove-service=dhcp && firewall-cmd --reload')
        print('Done\n')
        print('The DHCP server has been removed from your server\n')

    print('ITStudioLinux\nWelcome Install DHCP Server')
    selects = None
    while selects != '3':
        print('Select an item: \n 1. Install DHCP Server \n 2. Remove DHCP Server \n 3. Exit')
        selects = input('select [1-3]: ')
        if selects != '1' and selects != '2' and selects != '3':
            print(f"Sory, item {selects} is not in the list. \n")
        elif selects == '1':
            install_dhcp()
        elif selects == '2':
            removing_dhcp()
        elif selects == '3':
            print('Goodby')


if __name__ == "__main__":
    greeting()