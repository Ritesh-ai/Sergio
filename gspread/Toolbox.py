import os
import requests
import base64
from gspread import Client
from authlib.integrations.requests_client import AssertionSession
import csv
import json
import pandas as pd

# Set the Credentials.json in OS Environment
os.environ['credentials.json'] = "credentials.json"

class Toolbox():
	def __init__(self):
		self.GSHEET_SCOPES = [
			'https://spreadsheets.google.com/feeds',
			'https://www.googleapis.com/auth/drive',
			]
		# Get the Credentials.json from OS Environment
		self.GSHEET_CREDS  = os.environ['credentials.json']


	def gsheet_upload_csv(self, sh, sheet_name, sheet_id, content):
		self.SESSION = self.create_assertion_session_local()
		self.GCLI = Client(None, self.SESSION)
		self.WRKS = self.GCLI.open(sheet_name).sheet1

		## Import_csv function deletes all the sheets and re-write the data in first sheet
		self.GCLI.import_csv(sheet_id, content)


	def writeToGspreadMulti(self, sheet_title, listXLTabs, gsheet_id=None, sharelist=[]):
		"""
		To Create the Google Spread Sheet
		"""
		if gsheet_id is not None:
			self.SESSION = self.create_assertion_session_local()
			self.GCLI = Client(None, self.SESSION)
			sh = self.GCLI.open_by_key(gsheet_id)

			old_worksheets = [str(sheet).split("'")[1] for sheet in sh.worksheets()]

			for sheet in listXLTabs:
				df = pd.DataFrame(sheet['report_result'])
				cell_list = df.values.tolist()
				if sheet['report_name'] in old_worksheets:
					worksheet = sh.worksheet(sheet['report_name'])
					sh.values_update(
						sheet['report_name'],
						params={'valueInputOption': 'USER_ENTERED'},
						body={'values': cell_list}
					)
				else:
					sh.add_worksheet(title=sheet['report_name'], rows="100", cols="20")
					self.gsheet_upload_and_write_csv(sh, sheet['report_name'], sheet['report_result'])
			
		else:
			self.SESSION = self.create_assertion_session_local()
			self.GCLI = Client(None, self.SESSION)
			sh = self.GCLI.create(sheet_title)
			for email in sharelist:
				print(email)
				# To give the permission to the email ID.
				r = sh.share(email, perm_type='user', role='writer')
				print(r)
    		
			for sheet in listXLTabs:
				sh.add_worksheet(title=sheet['report_name'], rows="100", cols="20")
				self.gsheet_upload_and_write_csv(sh, sheet['report_name'], sheet['report_result'])

			worksheet = sh.worksheet("Sheet1")
			sh.del_worksheet(worksheet)

			# SpreadSheet Url
			url = "https://docs.google.com/spreadsheets/d/"+str(sh.id)
			
			return url


	def gsheet_upload_and_write_csv(self, sh, sheetname, datafile):
		"""
		Upload the CSV as WorkSheet in Google Spread Sheet
		"""
		df = pd.DataFrame(datafile)
		col = df.columns.values.tolist()
		val = df.values.tolist()
		data = [col] + val

		sh.values_update(
			sheetname,
			params={'valueInputOption': 'USER_ENTERED'},
			body={'values': data}
		)

	def create_assertion_session_local(self, subject=None):
		# conf = self.GSHEET_CREDS

		with open('credentials.json') as cred:
			conf = json.load(cred)
		
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

