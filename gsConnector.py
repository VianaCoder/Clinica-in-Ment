from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime;
import config;

class gsConnector:

    def __init__(self):
        self.creds_file = 'creds.json'
        self.scopes = config.gsheets['scopes']
        self.creds = service_account.Credentials.from_service_account_file(self.creds_file, scopes=self.scopes)
        self.pagId = None
        self.id = str(config.gsheets['link']).split("/")[5]
        
    def newUser(self, data):
        sheet = build('sheets', 'v4', credentials=self.creds).spreadsheets()
        today = datetime.now()
        try:
            sheet.values().append(
                spreadsheetId=self.id, 
                range='Users!A2',
                valueInputOption="USER_ENTERED", 
                body={'values':data}).execute()
            print("Adicionado")
        except Exception as e:
            print(str(today) + "-" + str(e) + "-" + str(data))
                
    def getUser(self):
        sheet = build('sheets', 'v4', credentials=self.creds).spreadsheets()
        today = datetime.now()
        try:
            data = sheet.values().get(
                spreadsheetId="12Ce0L641ZyV0oQQIF-3ZncrNBy0Lr1GhBDhokFwyAl8", 
                range='Users!A2:L').execute()
        except Exception as e:
            print(str(today) + "-" + str(e))
        return data['values']
    
    def setSchedule(self, data):
        sheet = build('sheets', 'v4', credentials=self.creds).spreadsheets()
        today = datetime.now()
        try:
            sheet.values().append(
                spreadsheetId=self.id, 
                range='Agendamentos!A2',
                valueInputOption="USER_ENTERED", 
                body={'values':data}).execute()
            print("Adicionado")
        except Exception as e:
            print(str(today) + "-" + str(e) + "-" + str(data))
            
    def getScheduled(self):
        sheet = build('sheets', 'v4', credentials=self.creds).spreadsheets()
        today = datetime.now()
        try:
            data = sheet.values().get(
                spreadsheetId="12Ce0L641ZyV0oQQIF-3ZncrNBy0Lr1GhBDhokFwyAl8", 
                range='Agendamentos!A:F').execute()
        except Exception as e:
            print(str(today) + "-" + str(e))
        return data['values']
    
    def getSchedule(self):
        sheet = build('sheets', 'v4', credentials=self.creds).spreadsheets()
        today = datetime.now()
        try:
            data = sheet.values().get(
                spreadsheetId="12Ce0L641ZyV0oQQIF-3ZncrNBy0Lr1GhBDhokFwyAl8", 
                range='Agendamentos!A2:B').execute()
        except Exception as e:
            print(str(today) + "-" + str(e))
        return data['values']

print(gsConnector().getScheduled())