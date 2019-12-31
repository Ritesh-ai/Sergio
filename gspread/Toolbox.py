import os
import requests
import base64
from gspread import Client, authorize
from authlib.integrations.requests_client import AssertionSession
from oauth2client.service_account import ServiceAccountCredentials
import csv

class Toolbox():
	def __init__(self):
		self.GSHEET_SCOPES = [
			'https://spreadsheets.google.com/feeds',
			'https://www.googleapis.com/auth/drive',
			]
		self.GSHEET_CREDS  = os.environ['credentials']

	def gsheet_upload_csv(self, sh, sheet_name, sheet_id, content):
		self.SESSION = self.create_assertion_session_local()
		self.GCLI = Client(None, self.SESSION)
		self.WRKS = self.GCLI.open(sheet_name).sheet1

		## Import_csv function deletes all the sheets and re-write the data in first sheet
		self.GCLI.import_csv(sheet_id, content)

	
	def gsheet_new_sheet(self, sheet_title, workSheetNames, sharelist = []):
		"""
		To Create the Google Spread Sheet
		"""

		self.SESSION = self.create_assertion_session_local()
		self.GCLI = Client(None, self.SESSION)
		sh = self.GCLI.create(sheet_title)
		for email in sharelist:
			print(email)
			# To give the permission to the email ID.
			r = sh.share(email, perm_type='user', role='writer')
			# print(r)

		for sheet in workSheetNames:
			sh.add_worksheet(title=sheet, rows="1000", cols="200")

		# sh.add_worksheet(title="Sheet2", rows="100", cols="20")
		# sh.add_worksheet(title="Sheet3", rows="100", cols="20")

		worksheet = sh.worksheet("Sheet1")
		sh.del_worksheet(worksheet)

		return sh

	def gsheet_upload_and_write_csv(self, sh, sheetname, csvfile):
		"""
		Upload the CSV as WorkSheet in Google Spread Sheet
		"""

		sh.values_update(
			sheetname,
			params={'valueInputOption': 'USER_ENTERED'},
			body={'values': list(csv.reader(open(csvfile)))}
		)
		
	# def gsheet_upload_and_write_csv(self, sh, spreadsheetId, sheetname):
	# 	"""
	# 	Upload the CSV as WorkSheet in Google Spread Sheet
	# 	"""

	# 	credentials = ServiceAccountCredentials.from_json_keyfile_name('Gspread-ee911af3b086.json', self.GSHEET_SCOPES)
	# 	client = authorize(credentials)

	# 	sh = client.open_by_key(spreadsheetId)
	# 	print(sheetname,"---------sheetname")
	# 	csvfile = "./files/"+sheetname+".csv"
	# 	print(csvfile,"-------------CSVfile")
		
	# 	sh.values_update(
	# 		sheetname,
	# 		params={'valueInputOption': 'USER_ENTERED'},
	# 		# body={'values': list(csv.reader(open(csvfile)))}
	# 		body={'values': list(csv.reader(open(csvfile)))}
	# 	)

	def create_assertion_session_local(self, subject=None):
		conf = self.GSHEET_CREDS
		token_url = conf['token_uri']
		issuer = conf['client_email']
		key = conf['private_key']
		key_id = conf.get('private_key_id')

		header = {'alg': 'RS256'}
		if key_id:
			header['kid'] = key_id

		# Google puts scope in payload
		claims = {'scope': ' '.join(self.GSHEET_SCOPES)}
		return AssertionSession(
			grant_type=AssertionSession.JWT_BEARER_GRANT_TYPE,
			token_url=token_url,
			token_endpoint="https://oauth2.googleapis.com/token",
			issuer=issuer,
			audience=token_url,
			claims=claims,
			subject=subject,
			key=key,
			header=header,
		)

