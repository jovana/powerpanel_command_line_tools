# -*- coding: utf-8 -*-
"""Class: powerpanel
    Functions for using in the PowerPanel Python app
"""

import json
import requests

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
                    "Content-Type": "application/json",
                    "ASYNC": "True"
                },
                data = p_JsonData
            )
        return response
