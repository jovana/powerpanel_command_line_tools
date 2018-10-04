import json
import requests
import class_powerpanel
import colors
import os
from collections import namedtuple
from pathlib import Path

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

        Make a choose of one of the following options:
        
        1. Domain info
        2. -- empty --
        3. -- emtpy --

        4. Exit / Quit
        """ + colors.bcolors.ENDC)
        
    selection = input("Please choose the number for the action you want to execute: ") 

    # init PowerPanel Class
    oPowerPanel = class_powerpanel.PowerPanel(api_key)

    if selection =='1':
        # Running domain info for the domains in file domain_list.txt

        # Ask if domain expireddate needs to update
        print(colors.bcolors.WARNING + """
        Do you want to udate the domain expiredate? [Default = N]
        Y = Yes
        N = No
        """+ colors.bcolors.ENDC) 
        update_expiredate = input("Please Select Y or N: ")

        # clear screen 
        os.system( 'clear' )  

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
        print( "delete")
    elif selection == '3':
        print("find") 
    elif selection == '4': 
        break
    else:
        print( "Unknown Option Selected!" )


