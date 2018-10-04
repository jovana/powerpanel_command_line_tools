# -*- coding: utf-8 -*-
"""Class: powerpanel
    Functions for using in the PowerPanel Python app
"""

import json
import requests
import colors
import os
from pathlib import Path

class PowerPanel:
    """ PowerPanel Class. Use this class in your Python app.

    Args:
        param1 (str): Your PowerPanel API key.
    """

    def __init__(self, p_APIKey):
        self.api_key = p_APIKey


    def apiCommand(self, p_RestCommand, p_JsonData):
        """ Made the API call to the PowerPanel API.

        Args:
            param1 (str): The restcommand eg. validate/ip.
            param2 (object): The json data object.
            param3 (int): The customer ID

        Returns:
            object: The return value. return the results of the requests.post command.
        """
        response = requests.post(
                url = "https://api.test.powerpanel.io/1.0/" + p_RestCommand,
                headers = {
                    "API_KEY": self.api_key,
                    #"cu_id": "1421",
                    "Content-Type": "application/json",
                    "ASYNC": "True"
                },
                data = p_JsonData
            )
        return response

    def loadListFromDisk(self, p_FileName):
        """ Loading data list needed for the bulk action.

        Args:
            param1 (str): The filename to open and read content.

        Returns:
            object: open().readLines() output
        """

        file_path = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), p_FileName)))
        if not file_path.is_file():
            print(colors.bcolors.FAIL + 'File name ' + p_FileName + ' not found!' + colors.bcolors.ENDC)
            print('For this action the the file with name: ' + p_FileName + ' is needed. Make sure you have created this file and add the content to.')
            self.file_contents = None
            return False
        else:
            print(colors.bcolors.WARNING + """
            Do you have added / update the correct content into the file: """ + p_FileName + """? [Default = N]
            Y = Yes
            N = No
            """+ colors.bcolors.ENDC) 
            file_updated = input("Please select Y or N: ") 
            if file_updated == 'Y':
                self.file_contents = open(p_FileName,"r").readlines()
                return True
            else:
                print(colors.bcolors.FAIL + 'Wrong or unsupported input given: ' + file_updated+ colors.bcolors.ENDC)
                self.file_contents = None
                return False

        
            
        