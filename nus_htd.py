import requests
import datetime
import random
import schedule
import sys
import time

class NUSHTD:
    def __init__(self, username, password):
        self.session = requests.Session()
        self.user = username[-4:]
        # specifying request url & payload
        response_type = "code"
        client_id = "97F0D1CACA7D41DE87538F9362924CCB-184318"
        resource = "sg_edu_nus_oauth"
        redirect_uri = "https://myaces.nus.edu.sg:443/htd/htd"
        auth_data = {
            "UserName": username,
            "Password": password,
            "authMethod": "FormsAuthentication"
        }
        auth_url = f"https://vafs.nus.edu.sg/adfs/oauth2/authorize?response_type={response_type}&client_id={client_id}&resource={resource}&redirect_uri={redirect_uri}"
        response = self.session.post(auth_url, data=auth_data)
        # check for logged in status
        if response.url.startswith(redirect_uri):
            self.isLoggedIn = True
            return
        self.isLoggedIn = False

    def declare(self, isAM, temperature):
        # check if user is authenticated
        if not self.isLoggedIn:
            return False, print("\nUser authentication failure!")

        declare_url = "https://myaces.nus.edu.sg/htd/htd"
        declare_data = {
            "actionName": "dlytemperature",
            "webdriverFlag": "",
            "tempDeclOn": datetime.datetime.now().strftime("%d/%m/%Y"),
            "declFrequency": "A" if isAM else "P",
            "symptomsFlag": "N",
            "familySymptomsFlag": "N",
            "temperature": temperature
        }
        response = self.session.post(declare_url, data=declare_data)
        if response.status_code == 200:
            print(
                f'\nSuccessfully declared temperature on {declare_data["tempDeclOn"]} ({declare_data["declFrequency"]}M) with {declare_data["temperature"]} for user ending {self.user}.')
        else:
            print('\nUnable to declare temperature.')

if (__name__ == "__main__"):
    nus_htd = NUSHTD("nusstu\\<NUSNET_ID>", "<PASSWORD>")
    temp = input("What temparature would you like to declare? ")
    currTime = datetime.datetime.now()
    if currTime.time() < datetime.time(12):
        nus_htd.declare(isAM = "A", temperature = temp)
    else:
        nus_htd.declare(isAM = "P", temperature = temp)