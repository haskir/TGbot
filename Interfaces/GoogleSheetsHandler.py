from pprint import pprint

import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from urllib.error import HTTPError


class GoogleSheetsHandler:
    Exist = False

    def __new__(cls, *args, **kwargs):
        """ SINGLETON """
        if not GoogleSheetsHandler.Exist:
            GoogleSheetsHandler.Exist = super().__new__(cls)
            return GoogleSheetsHandler.Exist
        return GoogleSheetsHandler.Exist

    def __init__(self, path_to_ini: str = "../cred.ini", scopes=None):
        """Shows basic usage of the Sheets API. Print values from a sample spreadsheet"""
        creds = None

        self.service_inner = None
        if scopes is None:
            scopes = ['https://www.googleapis.com/auth/spreadsheets']
        with open(path_to_ini, "r") as file:
            self.configs = dict()
            for string in file.readlines():
                self.configs[string.split("=")[0]] = string.split("=")[1].rstrip()

        self._SAMPLE_SPREADSHEET_ID = self.configs.get("sheet_id")
        self._CREDENTIALS_FILE = self.configs.get("account_creds")
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self._CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        self.service_inner = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    def show(self, spreadsheet_id: str = None, range: str = "A:1:E10", majorDimension: str = "COLUMNS"):
        # Пример чтения файла
        if not spreadsheet_id:
            spreadsheet_id = self._SAMPLE_SPREADSHEET_ID

        values = self.service_inner.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='A1:E10',
            majorDimension=majorDimension
        ).execute()
        pprint(values)

    def append(self, spreadsheet_id: str, data: list, category: str = "Sheet1"):
        values = {
            "values": [data]
        }
        try:
            response = self.service_inner.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=f"{category}!A1:Z1",
                valueInputOption="USER_ENTERED",
                insertDataOption="INSERT_ROWS",
                body=values).execute()
        except HTTPError as e:
            print(e)


if __name__ == "__main__":
    from GoogleDriveHandler import GoogleDriveHandler
    service = GoogleDriveHandler()
    uid = service.create("test")
    sheetHandler = GoogleSheetsHandler()
    service.create_permission(uid, "haskird2@gmail.com")
    data_in = [1, 2]
    sheetHandler.append(uid, data_in)
    input("Нажми Enter для удаления тестовой таблички")
    service.delete_tests()
