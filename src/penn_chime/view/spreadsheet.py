import gspread
from oauth2client.service_account import ServiceAccountCredentials

class spreadsheet:
    def __init__(self, st_obj, secret):
        self.st_obj = st_obj
        # use creds to create a client to interact with the Google Drive API
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        #secret = 'client_secret.json'
        #self.creds = ServiceAccountCredentials.from_json_keyfile_dict(secret)
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(secret, self.scope)
        self.client = gspread.authorize(self.creds)


    def createsheet(self, sheetname, header):
        sheet = None
        try:
            self.client.create(sheetname)
        except Exception as e:
            print("Caught exception " + e.__str__())
        try:
            sheet = self.client.open (sheetname).sheet1
            index = 0
            sheet.insert_row (header, index)
        except Exception as e:
            print("Caught exception " + e.__str__())
        return sheet

    def writeToSheet(self, sheetname, row):
        try:
            sheet = self.client.open (sheetname).sheet1
            list_of_hashes = sheet.get_all_records ( )
            currentrow = sheet.row_count
            sheet.insert_row (row, currentrow)
        except Exception as e:
            print("Caught exception " + e.__str__())

    def getAllRows(self, sheetname):
        allrows = None
        try:
            sheet = self.client.open (sheetname).sheet1
            allrows = sheet.get_all_records ( )
        except Exception as e:
            print("Caught exception " + e.__str__())
        return allrows