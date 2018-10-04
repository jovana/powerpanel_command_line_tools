import json
import requests
import class_powerpanel
import colors
import os
from collections import namedtuple
from pathlib import Path

# clear screen
os.system( 'clear' ) 

# loading config file
config_file = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.json')))

# Check if config files has found, if not print error and exit
if not config_file.is_file():
    print(colors.bcolors.FAIL + 'config.json not found!' + colors.bcolors.ENDC)
    print('Make sure you have a config file named config.json. This file contains also your API key.')
    exit()

# load config settings from config.json
config = json.load(open(config_file), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
api_key = config.api_key
selection = True

while selection: 

    print(colors.bcolors.OKBLUE + """
        -----------------------------
        ---- PowerPanel API tool ----
        -----------------------------

        Make a choice of one of the following options:
        
        1. Domain info (Sync domain information from the registry)
        2. Change domain name servers (Change the name server settings for your domains)
        3. Create DNS zones (Enabled DNS zones for the domains)

        4. Exit / Quit
        """ + colors.bcolors.ENDC)
        
    selection = input("Please choose the number for the action you want to execute: ") 

    # init PowerPanel Class
    oPowerPanel = class_powerpanel.PowerPanel(api_key)

    if selection =='1':
        # Running domain info for the domains in file domain_list.txt

        # clear screen 
        os.system( 'clear' ) 

        # Ask if domain expireddate needs to update
        print(colors.bcolors.WARNING + """
        Do you want to udate the domain expiredate? [Default = N]
        Y = Yes
        N = No
        """+ colors.bcolors.ENDC) 
        update_expiredate = input("Please Select Y or N: ") 

        if oPowerPanel.loadListFromDisk("domain_list.txt"):
            for domain in oPowerPanel.file_contents:                       
                print('Running getDomainInfo for domain: ' +domain)
                data = {}
                data["domainname"] = domain
                data['live'] = True
                if update_expiredate == 'Y':
                    data['update_subscription_date'] = True
                
                # Set API command
                response = oPowerPanel.apiCommand("Domain/info", json.dumps(data))
                response_json = json.loads(response.content.decode('UTF-8'))

                # print status from action
                if response_json['code'] == 1:
                    print(colors.bcolors.OKGREEN + 'Status: SUCCESS!\n' + response_json['msg'][0] + colors.bcolors.ENDC)
                else:
                    print(colors.bcolors.FAIL + 'Status: FAIL: ' +  response_json['msg'][0] + colors.bcolors.ENDC)
                print('========================================')
            print('Task done, returning to the menu...') 

    elif selection == '2':
        # Running change nameserver settings for the domains in file domain_list.txt

        # clear screen 
        os.system( 'clear' ) 

        # Ask if name server ID needs for the update
        print(colors.bcolors.WARNING + "Please enter the number of the name server set ID you want to use to update your domain.\nThis number can be found in the control panel." + colors.bcolors.ENDC) 
        try:
            nss_id = int(input("Please enter the number: "))
        except ValueError:
            nss_id = 0

        if not int(nss_id) > 0:
            print(colors.bcolors.FAIL +'Incorrect number given!' + colors.bcolors.ENDC)
            break

        if oPowerPanel.loadListFromDisk("domain_list.txt"):
            for domain in oPowerPanel.file_contents:                       
                print('Running domain modify for domain: ' +domain)
                data = {}
                data["domainname"] = domain
                data['nameserverset_id'] = nss_id
                
                # Set API command
                response = oPowerPanel.apiCommand("Domain/modify", json.dumps(data))
                response_json = json.loads(response.content.decode('UTF-8'))

                # print status from action
                if response_json['code'] == 1:
                    print(colors.bcolors.OKGREEN + 'Status: SUCCESS!\n' + response_json['msg'][0] + colors.bcolors.ENDC)
                else:
                    print(colors.bcolors.FAIL + 'Status: FAIL: ' +  response_json['msg'][0] + colors.bcolors.ENDC)
                print('========================================')
            print('Task done, returning to the menu...') 

    elif selection == '3':
        # Running create DNS zone for the domains in file domain_list.txt

        # clear screen 
        os.system( 'clear' ) 

        if oPowerPanel.loadListFromDisk("domain_list.txt"):
            for domain in oPowerPanel.file_contents:                       
                print('Create DNS zone for domain: ' +domain)
                data = {}
                data["domainname"] = domain
                
                # Set API command
                response = oPowerPanel.apiCommand("Dns/createZone", json.dumps(data))
                response_json = json.loads(response.content.decode('UTF-8'))

                # print status from action
                if response_json['code'] == 1:
                    print(colors.bcolors.OKGREEN + 'Status: SUCCESS!\n' + response_json['msg'][0] + colors.bcolors.ENDC)
                else:
                    print(colors.bcolors.FAIL + 'Status: FAIL: ' +  response_json['msg'][0] + colors.bcolors.ENDC)
                print('========================================')
            print('Task done, returning to the menu...') 

    elif selection == '4': 
        print(colors.bcolors.OKBLUE +  "Bye Bye!!" + colors.bcolors.ENDC)
        break
    else:
        print(colors.bcolors.FAIL +  "Unknown option selected, now exits!" + colors.bcolors.ENDC)


