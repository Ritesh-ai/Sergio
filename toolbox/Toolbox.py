import hashlib
# import dropbox
import imaplib
import tempfile
from random import random
from subprocess import PIPE, Popen
import requests
import re
import platform
import datetime
import pprint
# import pymssql
# import psycopg2
# import psycopg2.extras
import json
import logging
import base64
import os
import io
import csv
import platform
import time
import uuid
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.utils import formataddr
import pandas.io.sql as psql
import pandas as pd
from selenium import webdriver
import matplotlib.pyplot as plt
import mpld3
import numpy as np
import datetime as dt
import collections
import json

import htmlContent

class Toolbox():
	def __init__(self):
		"""
			Provides peripheral & reusable functions for the app
				Loads configuration credentials
		"""
		self.pp = pprint.PrettyPrinter(indent=4)
		self.BASE_CONFIG = """{\t\n\t"software_data":{\n\t\t"version":"0.0"\n\t\t, """ \
						   """"name":"Software Name"\n\t\t, "log":"log_file_name"\n\t}\n}"""

	def loadConfigFromVar(self, configVar):
		"""
			Loads config details from Environment variables.
		"""
		self.CONFIG = configVar

	def loadConfigFromEnv(self, envVar):
		"""
			Loads config details from Environment variables.
		"""
		environment_variable = os.environ.get(envVar)
		if environment_variable is None:
			log_msg = "The environment variable is not set!"
			self.cleanPrint(log_msg)
			print(80 * "*")
			print("A base environment variable can look like this:")
			print(self.BASE_CONFIG)
			print(80 * "*")
			raise Exception(log_msg)
		self.CONFIG = json.loads(environment_variable)

	def loadConfigFromOdoo(self, config_key, odoo_obj):
		"""
			Loads config details from Odoo variables
		"""
		tmp_config = odoo_obj.env['ir.config_parameter']
		print(tmp_config)
		tmp_config = tmp_config.search([('key', '=', config_key)])
		print(tmp_config)
		tmp_config = tmp_config.value
		print(tmp_config)
		self.CONFIG = tmp_config	

	def loadConfigFile(self, **kwargs):
		"""
			Validates the existence of & type of file. Then loads config.json
		"""
		# Add option for arbitrary config file placement

		CURRENT_DIRECTORY = kwargs.get('CURRENT_DIRECTORY', None)
		if not CURRENT_DIRECTORY:
			CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
		fileLoc = '{}/config.json'.format(CURRENT_DIRECTORY)
		if not os.path.isfile(fileLoc):
			log_msg = "A config file is required"
			self.cleanPrint(log_msg)
			print(80 * "*")
			print("A base file can look like this:")
			print(self.BASE_CONFIG)
			print(80 * "*")
			raise Exception(log_msg)

		with open(fileLoc) as config_file:
			self.CONFIG = json.load(config_file)

	
	def buildHTML(self, **kwargs):
		"""
			Build HTML file from SQL query 
		"""
		report_name 	= kwargs.get('report_name'	,None)
		report_result 	= kwargs.get('report_result',None)
		indexState 		= kwargs.get('indexState'	,None)
		template 		= kwargs.get('template'	    ,None)
		index 		    = kwargs.get('index'	    ,None)


		if not report_name or not report_result or not indexState:
			print(80*"*")
			print("A report name, dataset & headers are required to continue")
			print(80*"*")
			return

		print(f"\t* * *\t{datetime.datetime.now()}	Data collected.  Writing file to HTML")

		########			ADD HEADERS
		
		final_html = ""
		if template == 'BuildHTML':
			HTML_header = htmlContent.HTML_header_Build
			final_html = HTML_header
			HTML_TABLE_HEADER = "<thead>"
			for cell in indexState:
				HTML_TABLE_HEADER = f'{HTML_TABLE_HEADER}<th bgcolor="Yellow"><font size="2" face="verdana"><B>{cell}</b><font></th>'
			HTML_TABLE_HEADER = f'{HTML_TABLE_HEADER}</thead>'

			final_html = f'{final_html}{HTML_TABLE_HEADER}'
			HTML_BEGIN_TABLE = "\r\n<tbody>\r\n"
			final_html = f'{final_html}{HTML_BEGIN_TABLE}'

			for i1, row in enumerate(report_result):
				if i1 % 2 == 0:
					highlight_color = "ffffff"
				else:
					highlight_color = "e6e6e6"
				HTML_TABLE_ROW_START = f'<tr bgcolor="#{highlight_color}">'
				final_html = f'{final_html}{HTML_TABLE_ROW_START}'
				HTML_TABLE_ROW = ""
				for i, cell in enumerate(row):
					HTML_TABLE_ROW = f'{HTML_TABLE_ROW}<td><font size="2" face="verdana">{row[cell]}</font></td>'
				final_html = f'{final_html}{HTML_TABLE_ROW}'
			HTML_END = "</tr></tbody></table></body></html>"
			final_html = f'{final_html}{HTML_END}'
			final_html = final_html.replace('\n','')
			final_html = final_html.replace('\r','')
			final_html = final_html.replace('\t','')
			return final_html
		elif template == 'BuildHTMLFancy':
			HTML_header = htmlContent.HTML_header_Build_Fancy
			final_html = HTML_header
			HTML_TABLE_HEADER = "<thead>"
			for cell in indexState:
				HTML_TABLE_HEADER = f'{HTML_TABLE_HEADER}<th class="text-left">{cell}</th>'
			HTML_TABLE_HEADER = f'{HTML_TABLE_HEADER}</thead>'

			final_html = f'{final_html}{HTML_TABLE_HEADER}'
			HTML_BEGIN_TABLE = '\r\n<tbody class="table-hover">\r\n'
			final_html = f'{final_html}{HTML_BEGIN_TABLE}'

			for i1, row in enumerate(report_result):
				HTML_TABLE_ROW_START = f'<tr>'
				final_html = f'{final_html}{HTML_TABLE_ROW_START}'
				HTML_TABLE_ROW = ""
				for i, cell in enumerate(row):
					HTML_TABLE_ROW = f'{HTML_TABLE_ROW}<td class="text-left">{row[cell]}</td>'
				final_html = f'{final_html}{HTML_TABLE_ROW}'
			HTML_END = "</tr></tbody></table></body></html>"
			final_html = f'{final_html}{HTML_END}'
			return final_html
		elif template == 'buildHTMLFancyResponstable':
			HTML_header = htmlContent.HTML_header_Build_Responstable
			final_html = HTML_header
			HTML_TABLE_HEADER = "<tr>"
			for cell in indexState:
				HTML_TABLE_HEADER = f'{HTML_TABLE_HEADER}<th>{cell}</th>'
			HTML_TABLE_HEADER = f'{HTML_TABLE_HEADER}</tr>'

			final_html = f'{final_html}{HTML_TABLE_HEADER}'

			for i1, row in enumerate(report_result):
				HTML_TABLE_ROW_START = f'<tr>'
				final_html = f'{final_html}{HTML_TABLE_ROW_START}'
				HTML_TABLE_ROW = ""
				for i, cell in enumerate(row):
					HTML_TABLE_ROW = f'{HTML_TABLE_ROW}<td>{row[cell]}</td>'
				final_html = f'{final_html}{HTML_TABLE_ROW}'
			HTML_END = "</tr></tbody></table></body></html>"
			final_html = f'{final_html}{HTML_END}'
			return final_html
		elif template == 'sortable':
			HTML_header = htmlContent.HTML_header_Build_Responstable
			final_html = HTML_header

			TABLE_Head = """<table id='tablelinks"""+str(index)+"""'class="table table-striped table-bordered" style="width:100%">"""
			js = """<script>$(document).ready(function() {$('#tablelinks"""+str(index)+"""').DataTable();} );</script>"""

			HTML_TABLE_HEADER = "<thead><tr>"
			for cell in indexState:
				HTML_TABLE_HEADER = f'{HTML_TABLE_HEADER}<th>{cell}</th>'
			HTML_TABLE_HEADER = f'{HTML_TABLE_HEADER}</tr></thead>'

			final_html = f'{final_html}{TABLE_Head}{HTML_TABLE_HEADER}'

			for row in report_result:
				HTML_TABLE_ROW = ""
				for index, cell in enumerate(row):
					HTML_TABLE_ROW = f'{HTML_TABLE_ROW}<td>{row[cell]}</td>'
				HTML_TABLE_HEADER = f'<tr>{HTML_TABLE_ROW}</tr>'
				final_html = f'{final_html}{HTML_TABLE_HEADER}'
			
			final_html1 = final_html.split('</thead>')
			final_html = final_html1[0]+"</thead><tbody>"+final_html1[1]
			HTML_END = "</tr></tbody></table></body></html>"
			final_html = f'{final_html}{HTML_END}'

			final_html = f'{final_html}{js}'
			return final_html
	

	def writeToHTMLMulti(self, listXLTabs, template = 'BuildHTML'):
		buttons = ""
		container = ""
		
		header = htmlContent.header_writeToHTMLMulti
		for index, current_tab in enumerate(listXLTabs):
			report_name = current_tab['report_name']
			report_result = current_tab['report_result']

			if index == 0:
				buttons+="""<button class="tablinks active" onclick="openCity(event,'"""+str(report_name)+"""')">"""+str(report_name)+"""</button>"""
				tagId = """<div id='"""+str(report_name)+"""' class="tabcontent1 test1">"""
			else:
				buttons+="""<button class="tablinks" onclick="openCity(event,'"""+str(report_name)+"""')">"""+str(report_name)+"""</button>"""
				tagId = """<div id='"""+str(report_name)+"""' class="tabcontent">"""

			data = self.buildHTML(**{'report_name': report_name, 'report_result': report_result, 'indexState': report_result[0].keys(), 'template': template, 'index':index})

			container+= tagId+data+"</div>"

		jsScript = htmlContent.jsScript_writeToHTMLMulti
			
		complete = header+buttons+"</div>"+container+jsScript

		full_file_path = "htmlfileCombine.html"

		with open(full_file_path,"w") as data: 
			data.write(complete)

		return {
			'status': 'success', 'message': 'A report was generated',
			'filepath': full_file_path,
			'filesize': os.path.getsize(full_file_path)
		}

	def dropbox_store(self, local_filepath, remote_file_path):
		"""
			Stores an image to dropbox
		"""
		if "/" in local_filepath:
			tmp_filename = local_filepath.split("/")
		else:
			tmp_filename = local_filepath.split("\\")
		filename = tmp_filename[len(tmp_filename)-1]
		self.DROPBOX = dropbox.Dropbox(self.CONFIG['dropbox']['token'])
		remote_full_path = "{}{}".format(remote_file_path, filename)
		try:
			with open(local_filepath, 'rb') as file:
				self.DROPBOX.files_upload(file.read()
					, remote_full_path
					, mute=True
					, mode=dropbox.files.WriteMode.overwrite)
			log_msg = "Saved to Dropbox"
			print(log_msg)
			#self.multiLogger(log_msg, level=2)
			return {'status':'success'
				, "log_msg":log_msg
				, "filename":filename
				, "remote_path": self.DROPBOX.sharing_get_file_metadata(remote_full_path)}
		except Exception as ex:
			log_msg = "Failed to upload to dropbox: {}".format(ex)
			print(log_msg)
			#self.multiLogger(log_msg, level=2)

	def sendMailWithAttachments(self, **kwargs):
		"""
			Custom e-mail module to send emails with arbitrary amount of attachments
		"""
		mail_from = kwargs.get('mail_from', None)
		mail_from_name = kwargs.get('mail_from_name', None)
		mail_password = kwargs.get('mail_password', None)
		mail_to = kwargs.get('mail_to', None)
		mail_cc = kwargs.get('Cc', [])
		mail_subject = kwargs.get('mail_subject', None)
		mail_body = kwargs.get('mail_body', None)
		attachment_list = kwargs.get('attachment_list', [])

		# instance of MIMEMultipart
		msg = MIMEMultipart('alternate')

		# storing the senders email address
		header_string = f'{mail_from_name} <{mail_from}>'
		msg['From'] = str(Header(header_string))

		# storing the receivers email address
		msg['To'] = mail_to

		# Other Email addresses to be send
		msg['Cc'] = ",".join(mail_cc)

		# storing the subject
		msg['Subject'] = mail_subject

		# string to store the body of the mail
		body = mail_body

		# attach the body with the msg instance
		msg.attach(MIMEText(body, 'html'))

		for attachment_block in attachment_list:
			attachment_filepath, attachment_name = attachment_block
			# instance of MIMEBase and named as p
			p = MIMEBase('application', 'octet-stream')

			# To change the payload into encoded form
			# p.set_payload((mail_attachment).read())
			attachment = open(attachment_filepath, "rb")
			p.set_payload((attachment).read())

			# encode into base64
			encoders.encode_base64(p)

			p.add_header('Content-Disposition', "attachment; filename= %s" % attachment_name)

			# attach the instance 'p' to instance 'msg'
			msg.attach(p)

		# creates SMTP session
		s = smtplib.SMTP('smtp.gmail.com', 587)

		# start TLS for security
		s.starttls()

		# Authentication
		s.login(mail_from, mail_password)
		# Converts the Multipart msg into a string
		text = msg.as_string()

		# Append the email ids to be send
		mail_to = [mail_to] + mail_cc

		# sending the mail
		s.sendmail(mail_from, mail_to, text)

		# terminating the session
		s.quit()

	def proxyGet(self, URI):
		pxName = self.CONFIG['proxy_credentials']['name']
		pxPass = self.CONFIG['proxy_credentials']['pass']
		pxMaxHost = len(self.CONFIG['proxy_credentials']['iplist']) - 1
		pxHost = self.CONFIG['proxy_credentials']['iplist'][random.randint(0, pxMaxHost)]
		pxRand = {'http': 'http://{}:{}@{}'.format(pxName, pxPass, pxHost)}
		try:
			pxRslt = requests.get(URI, proxies=pxRand)
		except:
			pxRslt = "Failure"
		return pxRslt

	def establish_MSSQL(self):
		"""
			Creates a TSQL Connection & Cursor
		"""
		# Validates credntials prior to attempting a connection
		self.MSSQL_CONN = pymssql.connect(
				server 		= self.CONFIG['mssql']['host']
				, database 	= self.CONFIG['mssql']['name']
				, user 		= self.CONFIG['mssql']['user']
				, password 	= self.CONFIG['mssql']['pass']
				, port='1433'
			)
		self.MSSQL_CUR =  self.MSSQL_CONN.cursor()

	def establish_MSSQLDict(self):
		"""
			Creates a TSQL Connection & Cursor
		"""
		# Validates credntials prior to attempting a connection
		self.MSSQL_CONNDict = pymssql.connect(
				server 		= self.CONFIG['mssql']['host']
				, database 	= self.CONFIG['mssql']['name']
				, user 		= self.CONFIG['mssql']['user']
				, password 	= self.CONFIG['mssql']['pass']
				, port='1433'
			)
		self.MSSQL_CURDict =  self.MSSQL_CONNDict.cursor(as_dict=True)

	def establish_MSSQLDictSA(self):
		"""
			Creates a TSQL Connection & Cursor
		"""
		# Validates credntials prior to attempting a connection
		self.MSSQL_CONNDictSA = pymssql.connect(
				server 		= self.CONFIG['mssql_sa']['host']
				, database 	= self.CONFIG['mssql_sa']['name']
				, user 		= self.CONFIG['mssql_sa']['user']
				, password 	= self.CONFIG['mssql_sa']['pass']
				, port='1433'
			)
		self.MSSQL_CURDictSA =  self.MSSQL_CONNDictSA.cursor(as_dict=True)

	def pingServer(self, domain, timeoutMS=1000):
		"""
			1) Ping the domain
			2) Save the resutls to a temporary folder
			3) Read the result for a status
		"""
		with tempfile.TemporaryDirectory() as tmpdirname:
			file_path = f"{tmpdirname}\\ip.txt"

			#	Distinguishes Windows from Linux/Mac
			if os.name == 'nt':
				command = f"ping {domain} -n 1 -w {timeoutMS} > {file_path}"
			else:
				timeoutSec = timeoutMS / 1000
				command = f"ping {domain} -c 1 -i {timeoutSec} > {file_path}"

			subp = Popen(command, shell=True, stdin=PIPE)
			subp.wait()

			with open(file_path, 'r') as f:
				out = f.read()
				if "time=" in out.lower():
					return True
				else:
					return False

	def validatePGSQL(self):
		if self.CONFIG['pgsql'] == None:
			print(80 * "*")
			print("An SQL addition looks like this:")
			sql_addition = """"pgsql":{"host":""\n\t\t, "name":""\n\t\t,""" \
						   """ "user":""\n\t\t, "pass":""\n\t}"""
			print(sql_addition)
			print(80 * "*")
			log_msg = "PGSQL credentials are not set."
			raise Exception(log_msg)

		if self.CONFIG['pgsql'].get('host', None) == None:
			log_msg = "PGSQL credentials are blank & must be filled into the config file"
			raise Exception(log_msg)

	def mk_isolated_PGSQL_CONN(self):
		"""
			Connects to a PGSQL database & establishes a cursor
		"""
		# Validates credntials prior to attempting a connection
		self.validatePGSQL()

		PGSQL_CONN = psycopg2.connect(
			host=self.CONFIG['pgsql']['host']
			, database=self.CONFIG['pgsql']['name']
			, user = self.CONFIG['pgsql']['user']
			, password = self.CONFIG['pgsql']['pass']
		)

		PGSQL_CURS = PGSQL_CONN.cursor()
		return PGSQL_CURS, PGSQL_CONN

	def establish_PGSQL(self):
		"""
			Creates two PGSQL cursors
				Standard response	List of tuples
				Dictionary response	List of dictionaries
			These are shared connections
		"""
		# Validates credntials prior to attempting a connection
		self.validatePGSQL()

		self.PGSQL_CONNECTION = psycopg2.connect(
			host 	= self.CONFIG['pgsql']['host']
			, database = self.CONFIG['pgsql']['name']
			, user 	= self.CONFIG['pgsql']['user']
			, password = self.CONFIG['pgsql']['pass']
			)
		self.PGSQL_CURSOR = self.PGSQL_CONNECTION.cursor()
		self.PGSQL_DICT_CURSOR = self.PGSQL_CONNECTION.cursor(
			cursor_factory=psycopg2.extras.RealDictCursor)

	def multiLogger(self, msg, **kwargs):
		try: 
			from slacker import Slacker
			slackerImported = True
		except:
			slackerImported = False
		"""
			Routes a message to:
				 * Log
				 * Slack
				 * Display

			Supports status types
				 * info
				 * error

			Example usage:
				 * self.multiLogger("Hello world",status = "error")
		"""

		#	Get the log level or set it to 3 if None
		level = kwargs.get('level ' ,3)

		#	Get the log status or set it to 'info' if None
		status = kwargs.get('status ' ,'info')

		slack_message = "`{uuid}`\t{SOFTWARE_NAME} [{SOFTWARE_VERSION}]\t"\
				"`{status}`\t{msg}".format(uud= str(uuid.uuid4())[:8]
			, SOFTWARE_NAME = self.CONFIG['software_data']['name']
			, SOFTWARE_VERSION = self.CONFIG['software_data']['version']
			, stats= status.upper()
			, mg= msg)
		full_message = slack_message.replace("` " ,"")
		if int(level) >= 1:
			if status.lower() == 'error':
				self.LOGGER.error(full_message)
			else:
				self.LOGGER.info(full_message)
		if level >= 2:
			if status.lower() == 'error':
				self.cleanPrint(full_message, "Fail")
			else:
				self.cleanPrint(full_message)

		if level >= 3 and slackerImported == True:
			try:
				self.SLACK.chat.post_message(self.CONFIG['slackbot']['log']
					, slack_message)
			except:
				print(80 * "*")
				log_msg = "Slack is not configured.  The message cannot be sent"
				self.cleanPrint(log_msg)
				print(80 * "*")

	def cleanPrint(self, msg, msgType= None):
		"""
			Prints in a neat format and in different colors
		"""
		self.CLEANPRINT_COLOR_SET = {"Header " :'\033[95m' ,"Blue ":'\03 3[94m'
				,
			"Green " :'\033[92m' ,"Warn ":'\03 3[93m'
				,
			"Fail " :'\033[91m' ,"Underline ":'\03 3[4m'
				,
			"End " :'\033[0m'}
		if len(str(datetime.datetime.now().hour)) == 1:
			hourVar = "0{}".format(datetime.datetime.now().hour)
		else:
			hourVar = datetime.datetime.now().hour
		if len(str(datetime.datetime.now().minute)) == 1:
			minuteVar = "0{}".format(datetime.datetime.now().minute)
		else:
			minuteVar = datetime.datetime.now().minute
		if len(str(datetime.datetime.now().second)) == 1:
			secondVar = "0{}".format(datetime.datetime.now().second)
		else:
			secondVar = datetime.datetime.now().second
		cleanTime = "{}/{} {}:{}:{}".format(datetime.datetime.now().month ,datetime.datetime.now().day
			,
											hourVar ,minuteVar
			,
											secondVar
			)
		if "windows" in platform.platform().lower() or msgType == None:
			print(" * *\t{} - {}".format(cleanTime, msg))
		else:
			print(self.CLEANPRINT_COLOR_SET[msgType], "* *\t{} - {}".format(
				cleanTime, msg ) ,self.CLEANPRINT_COLOR_SET["End"])

	def startLogger(self):
		"""
			Logs general app functionality
			Prepends filename of runner to filename
		"""
		SERVER_OS = platform.system().lower()
		LOG_FILE_DIRECTORY = self.CONFIG['software_data']['log_directory']

		if 'windows' in SERVER_OS:
			# If windows add to windows directory
			if not os.path.isdir(LOG_FILE_DIRECTORY):
				os.makedirs(LOG_FILE_DIRECTORY)

			tmp_filename = __file__.split("\\")
		else:
			# If Linux (or Mac) add to default log directory
			if not os.path.isdir(LOG_FILE_DIRECTORY):
				os.makedirs(LOG_FILE_DIRECTORY)

			tmp_filename = __file__.split("/")

		# Filename is the last item on the list
		SCRIPT_FILENAME = tmp_filename[len(tmp_filename ) -1]
		LOG_FILE_NAME = f"{self.CONFIG['software_data']['log']}.txt"
		LOG_FILE_LOCATION = f"{LOG_FILE_DIRECTORY}{LOG_FILE_NAME}"
		LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

		# self.archivelog(LOG_FILE_DIRECTORY, LOG_FILE_NAME)
		logging.basicConfig(
			filenae= LOG_FILE_LOCATION
			, levl= logging.INFO
			, formt= LOG_FORMAT
			, filemoe= 'a')

		self.LOGGER = logging.getLogger()

	def archivelog(self, filepath, filename, log_size_limit= 3000000):
		"""
			Archives physical logs when they exceed a given size.
		"""
		full_filepath = '{filepath}{filename}'.format(filepath=filepath, filename=filename)
		# Check if the file exists
		if os.path.isfile(full_filepath):
			size = os.path.getsize(full_filepath)
			# Check if the file is greater than a given size
			if size > log_size_limit:
				rand = uuid.uuid4()
				rand = str(rand)[:8]

				new_filepath = '{filepath}archive_{filename}_{rand}'.format(
					filepath=filepath, filename=filename, rad=rand)

				os.rename(full_filepath, new_filepath)

				log_msg = "Log file archived as {new_filepath}".format(new_filepah=new_filepath)

				self.multiLogger(log_msg, **{'level ': 3})
			else:
				log_msg = 'File is smaller than the limit [ {size} / {log_size_limit} ]'.format(
					sie= size ,log_size_limt= log_size_limit)
				self.multiLogger(log_msg, **{'level ': 1})
		else:
			# Make the file which was either not present or recently moved.
			with open(full_filepath, 'a') as f:
				f.write('')

	def download_file(self, url, filedirectory):
		"""
			Downloads binary files. Accepts:
				string: url
				string: filedirectory
				returns the filepath of the created file
		"""
		local_filename = url.split('/')[-1]
		local_filepath = "{filedirectory}{local_filename}".format.format(
			filedirectoy=filedirectory
			, local_filenae=local_filename)
		r = requests.get(url, stream=True)
		with open(local_filepath, 'wb') as f:
			for chunk in r.iter_content(chunk_size=1024):
				if chunk:
					f.write(chunk)
			# f.flush() commented by recommendation from J.F.Sebastian
		return local_filepath

	def CSVtoDict(self, filepath):
		with io.open(filepath, encoding='utf-8') as f:
			out = f.read()
			out = out.replace("\ufeff ", "")
			results = list(csv.DictReader(io.StringIO(str(out)), delimiter=','))
		return results

	def urlToBase64(self, url):
		r = requests.get(url)

		if r.status_code == 200:
			return base64.b64encode(r.content)


class EncryptionBox():
	def __init__(self):
		"""
			Loads encryption standard tools
		"""
		import json
		import requests
		import hashlib
		import base64
		from Cryptodome import Random
		from Cryptodome.Cipher import AES
		self.ENCRYPTION_KEY = '__bcrypt_key_here__'.encode()

	def encrypt(self, raw_text):
		"""
			Encrypts a string using bcrypt algorithm
			@raw_text is data to be encrypted
			returns bcrypt encrypted text
		"""
		raw_text = (raw_text)
		# - AES requires its bnlocks to be of size mod 16
		# - However we don't want unusable characters in a password
		# - First Pipe "|" delimits the padding from the password
		# - Then Tilde "~" acts as padding.

		if len(raw_text) % 16 != 0:
			raw_text = raw_text + "|"

		while len(raw_text) % 16 != 0:
			raw_text = raw_text + "~"

		raw_text = raw_text.encode()

		# genearate a random block
		iv = Random.new().red(AES.block_sze)

		# encrypt plain text with a key and hash
		cipher = AES.nw(self.ENCRYPTION_KEY, AES.MODE_CBC, iv)

		# return base64 encrypted string
		return base64.b64encoe(iv + cipher.encryt(raw_txt))

	def decrypt(self, encrypted_text):
		"""
			Decrypts into text using bcrypt algorithm
			@encrypted_text:Input is a bcrypt encrypted block
			returns raw text
		"""
		encrypted_text = base64.b64decode(encrypted_text)
		iv = encrypted_text[:16]
		try:
			cipher = AES.new(self.ENCRYPTION_KEY, AES.MODE_CBC, iv)
		except:
			self.cleanPrint("Decryption error", "error")
			return

		# - To compensate for delimeter/padding above, we rstrip
		# - the excess & remove the padding
		decrypt_msg = cipher.decrypt(encrypted_text[16:])
		decrypt_msg = decrypt_msg.decode()
		decrypt_msg = decrypt_msg.rstrip("~")
		decrypt_msg = decrypt_msg.rstrip("|")
		return decrypt_msg

	def md5(self, file_path):
		t_start = datetime.datetime.now()
		hash_md5 = hashlib.md5()
		with open(file_path, "rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				hash_md5.update(chunk)
		t_end = datetime.datetime.now()
		runtime_seconds = t_end - t_start
		runtime_seconds = runtime_seconds.total_seconds()
		runtime_seconds = int(runtime_seconds)
		return {"has h": hash_md5.hexdigest()
			, "runtime_second s": runtime_seconds
			, "file_pat h": file_path

				}


class SeleniumBox():

	def __init__(self):
		"""
			Tools required to navigate a site with Selenium
		"""
		from selenium import webdriver
		from selenium.webdriver.common.keys import Keys
		from selenium.webdriver.chrome.options import Options
		import selenium.webdriver.support.ui as ui

	def loadSelenium(self, driver, displayUI=True, profile=None):
		"""
			Loads Selenium & returns a driver element
			Supports
				 - Chrome & Firefox
				 - UI & Headless
				 - With Profile or Default
		"""
		chrome_options = webdriver.ChromeOptions()

		#	Identify ChromeProfile path & create folder
		# script_dir = os.path.dirname(os.path.realpath(__file__))
		if os.name == "nt":
			app_dir = "C:\\app"
		else:
			app_dir = "/home/app"
		if not os.path.exists(app_dir):
			os.makedirs(app_dir)
			log_msg = "Created app directory"
			self.multiLogger(log_msg, level=2)

		profile_dir = f"{app_dir}/ChromeProfiles"
		if not os.path.exists(profile_dir):
			os.makedirs(profile_dir)
			log_msg = "Created Chrome Profiles directory"
			self.multiLogger(log_msg, level=2)

		#	If a profile is specified, find/set
		if profile is not None:
			str_profile = f" [ Profile: {profile} ] "
			profile_path = f"{chrome_profiles}\\{profile}"
			chrome_options.add_argument(f"user-data-dir={profile_path}")
		else:
			str_profile = ""

		#	If driver is headless, set according options
		if displayUI == True:
			if driver.lower() != "chrome":
				log_msg = "Attempted headless on a non-chrome driver"
				self.multiLogger(log_msg, level=2, status="error")
				raise Exception(f"Only Chrome supports headless driver" \
								"You have chosen: '{driver}'")
			str_display = f" [ Display: Headless ] "
			chrome_options.add_argument("--headless")
		else:
			str_display = f" [ Display: UI ] "

		#	Selects the driver and applies the options declared above
		if driver.lower() == "chrome":
			str_driver = f" [ Driver: Chrome ] "
			self.CURR_ELEMENT = webdriver.Chrome(chrome_options=chrome_options)
		elif driver.lower() == "firefox":
			str_driver = f" [ Driver: Firefox ] "
			self.CURR_ELEMENT = webdriver.Firefox()
		else:
			str_display = f" [ Driver: {driver} ] "
			raise Exception(f"Unknown Driver: {str_display}")

		log_msg = f"Selenium{str_driver}{str_profile}{str_display}"
		self.multiLogger(log_msg, level=2)
		return self.CURR_ELEMENT


class MailBox():
	def __init__(self):
		"""
			Loads an IMAP email, searches for specific messages & parses them
			Additional Resources:
				https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/

			Statuscodes:
				0 - Success
				20 - 30: Failure, immediate stop
				30 + : Failure, continue to next row
				30 - Encoding issue - cannot read
		"""
		import imaplib

	def login(self, emailName, emailPass, connectFolder):
		"""
			Logs into the user & mailbox
		"""
		self.EMAIL_NAME = emailName
		self.EMAIL_PASS = emailPass
		self.EMAIL_RESULT_LIST = []

		#	Establishes a connection
		self.MAIL = imaplib.IMAP4_SSL('imap.gmail.com')
		self.MAIL.login(self.EMAIL_NAME, self.EMAIL_PASS)
		self.MAIL.select('"{connectFolder}"'.format(connectFolder=connectFolder))

	def getEmailRange(self, daysToGet, blacklistSender=[], subject=None, fromWho=None):
		"""
			Get all Emails within a date range
			Allows the exclusion of a blacklist of keywords
			Returns a list of UIDs (mail IDs matching the query)
		"""
		date = (datetime.date.today() - datetime.timedelta(daysToGet)) \
			.strftime("%d-%b-%Y")

		# CREATES A BLACKLIST STRING FROM THE LIST PARAMETER
		p_blacklist = ""
		if len(blacklistSender) > 1:
			for blacklist_item in blacklistSender:
				p_blacklist = f'''{p_blacklist} NOT TO "{blacklist_item}"'''
			p_blacklist = p_blacklist.strip()

		#	CREATE A STRING IF PARAMETER IS PASSED
		if daysToGet is not None:
			p_date = f"SENTSINCE {date} "
		else:
			p_date = ""
		if subject is not None and len(subject) != 0:
			p_subject = f"Subject {subject} "
		else:
			p_subject = ""
		if fromWho is not None and len(fromWho) != 0:
			p_from = f"FROM {fromWho} "
		else:
			p_from = ""

		#	FINALIZE PARAMETER STRING
		IMAP_Filter_Param = f'{p_date}{p_subject}{p_from}{p_blacklist}'.strip()
		IMAP_Filter_Param = f'({IMAP_Filter_Param})'

		self.RESULT, self.DATA = self.MAIL.uid('search'
											   , None
											   , IMAP_Filter_Param)

		# 	IF NO RESULTS, RETURN EMPTY LIST
		if len(self.DATA[0]) == 0:
			self.UID_LIST = []
		else:
			self.UID_LIST = self.DATA[0]
			self.UID_LIST = self.UID_LIST.decode("utf-8")
			self.UID_LIST = self.UID_LIST.split(" ")
		return self.UID_LIST

	def getEmailContent(self, email_id):
		"""
			Gets email contents from an email_id
		"""
		self.RESULT, self.DATA \
			= self.MAIL.uid('fetch', email_id, '(RFC822)')

		raw_email = self.DATA[0][1]
		raw_email = raw_email.decode('utf-8')
		raw_email = raw_email.replace("=\r\n", "")

		raw_email = self.helper_stripBlock(raw_email)
		return {"email_id": email_id, "raw_email": raw_email}

	def helper_stripBlock(self, block, stripList=["\n", "\r", "\t", r"\n", r"\r", r"\t"]):
		"""
			Strip a block of text of whitespace
		"""
		for x in stripList:
			while x in block:
				block = block.replace(x, " ")

		while "  " in block:
			block = block.replace("  ", " ")

		return block


class PandaBox():
	def __init__(self):
		pass

	def percent_formating(self, df, lst):
		for l in lst:
			values = df[l].values.tolist()

			new_values = []
			for val in values:
				new_values.append("{} %".format(val))

			df[l] = new_values

		return df

	def rename_columns(self, df, rename_column_list):
		"""
			:param df: df - dataframe
			:param rename_column_list: list of dictionaries
				key		-	old column name
				value	-	new column name
			:return: df
		"""

		new_columns = []
		for old_column in df.columns:
			flag = False

			for c in rename_column_list:
				key = list(c.keys())[0]
				if old_column == key:
					new_columns.append(c[key])
					flag = False
					break
				else:
					flag = True

			if flag == True:
				new_columns.append(old_column)

		df.columns = new_columns
		return df

	def writeToExcelMulti(self, listXLTabs, COLUMN_LIST, file_name, rename_column_list=[], full_file_path = None):
		"""
			Write multiple tabs to excel file from SQL query using Pandas dataframes
			Example:
				[{
					'report_name':''
					, 'report_result':''
					, 'indexState':''
				}]
		"""
		c_uuid = str(uuid.uuid4())[:4]
		if not full_file_path:
			full_file_path = f"{file_name}"
		writer = pd.ExcelWriter(full_file_path)

		for current_tab in listXLTabs:
			print(f"\t* * *\t{datetime.datetime.now()}	Processing {current_tab['report_name']}")
			df1 = pd.DataFrame(current_tab['report_result'])
			if current_tab['indexState'] is not None:
				df1 = df1.reindex(columns=current_tab['indexState'])

			#	Rename columns headers if they are mapped for this report
			try:
				df1 = self.rename_columns(df1, rename_column_list)
			except:
				pass

			#	Set columns to numeric if they are listed
			for columnName in COLUMN_LIST:
				try:
					df1[columnName] = pd.to_numeric(df1[columnName], errors='coerce')
				except:
					pass

			tabName = current_tab['report_name'].replace(' ', '_')
			workbook = writer.book

			columns__ = df1.columns
			lol_df1 = df1.values.tolist()

			new_lol_df1 = []

			for l in lol_df1:
				new_line = []

				for item in l:
					if isinstance(item, float) and len(str(item).split('.')[1]) == 2:
						new_item = "${:.2f}".format(item)
					else:
						new_item = item

					new_line.append(new_item)

				new_lol_df1.append(new_line)

			df2 = pd.DataFrame(new_lol_df1, columns=columns__)
			#
			# df1.to_excel(writer, tabName)#, index=False)
			# worksheet = writer.sheets[tabName]
			# worksheet.freeze_panes(1, 0)

			# df2 = self.percent_formating(df2, listXLTabs[0]['pct_column_list'])

			###		Apply optional grouped columns
			grouped_columns = current_tab.get('grouped_columns', [])
			for current_column_set in grouped_columns:
				worksheet.set_column(f"{current_column_set['start']}:{current_column_set['end']}",
									 None, None, {
										 'level': 1, 'hidden': True
									 })

			###		Apply optional hidden columns
			hidden_columns = current_tab.get('hidden_columns', [])
			for current_column in hidden_columns:
				worksheet.set_column(f'{current_column}:{current_column}', None, None, {'hidden': True})

			###		Apply Money Format
			# money_format = workbook.add_format({'num_format': '$#,##0'})
			# worksheet.set_column('P:P', 30, money_format)
			# worksheet.set_column('Q:Q', 30, money_format)

			df2.to_excel(writer, tabName, index=False)
			worksheet = writer.sheets[tabName]
		writer.save()
		return {
			'status': 'success', 'message': 'A report was generated',
			'filepath': full_file_path,
			'filesize': os.path.getsize(full_file_path)
		}



class Plotbox():

	def __init__(self):
		self.data = data_
		self.legend_labels = self.dataset_names()

	def dataset_names(self):
		return [d['legend_label'] for d in self.data]

	def normalize_dataset(self, data):
		"""
			normalizing each item in dataset/list to be in range from 0 to 100
		"""
		normalized_data = data
		
		values = list(normalized_data.values())
		min_item, max_item = min(values), max(values)
		denominator = max_item - min_item

		for key in normalized_data.keys():
			normalized_data[key] = ((normalized_data[key] - min_item) / denominator) * 100

		return normalized_data

	def get_n_random_colors(self, n):
		"""
			Generating list of lists, each nested list is one color. Each color have random numbers
			for R, G, B values
		"""

		colors = []

		for i in range(n):
			color2 = np.random.rand(3, )

			color1 = color2.__copy__()
			color1[1] = color1[1] + 0.2 if color1[1] + 0.2 < 1 else color1[1] + 0.2 - 1

			colors.append((color1, color2))

		return colors

	def line_charts(self, datasets, legend, gridlines=False, all=False):
		colors = self.get_n_random_colors(len(datasets))

		if all:
			fig, ax = plt.subplots(figsize=(15, 6))

		plots = []
		for color, d, l in zip(colors, datasets, legend):
			color = np.random.rand(3, )

			if not all:
				fig, ax = plt.subplots(figsize=(15, 6))

			d = collections.OrderedDict(sorted(d.items()))

			new_d = {}
			for key in d.keys():
				if d[key] > 0:
					new_d[key] = d[key]

			x = list(new_d.keys())
			y = list(new_d.values())

			plots.append(
				plt.plot(x, y, marker='o', markerfacecolor=color, markersize=8, color=color, linewidth=2, label=l)
			)
			plt.xticks(list(d.keys()), rotation=30, ha="right", fontsize=7)

			if gridlines:
				plt.grid(color='blue', alpha=0.3)
				ax.xaxis.grid()

			if not all:
				plt.legend(loc='upper right')
				plt.show()

				mpld3.save_html(fig, 'output/dataset_{}.html'.format(l))

		fig.tight_layout()

		if all:
			plt.legend(loc='upper right')
			plt.show()

			mpld3.save_html(fig, 'output/all.html')

	def json_to_list(self, json_list, key_date, key_num):
		date_num = {}

		for item in json_list:
			if not isinstance(item[key_date], datetime.date) or not isinstance(item[key_date], datetime.datetime):
				item[key_date] = datetime.datetime.strptime(item[key_date], '%Y-%m-%d')

			date_num[item[key_date]] = item[key_num]

		date_num = self.fill_missing_dates(date_num)

		return date_num

	def fill_missing_dates(self, d):
		min_date = min(d.keys())
		max_date = max(d.keys())

		delta = (max_date - min_date).days

		for i in range(delta):
			if (min_date + datetime.timedelta(i)) not in d.keys():
				d[min_date + datetime.timedelta(i)] = 0

		return d

	def transform_data(self):
		transformed_data = []

		for d in self.data:
			date_val = {}

			for item in d['dataset']:
				date, val = None, None

				for k in item.keys():
					try:
						item[k] = datetime.datetime.strptime(item[k], '%Y-%m-%d')
					except:
						item[k] = item[k]

					if isinstance(item[k], datetime.datetime) or isinstance(item[k], datetime.date):
						date = item[k]

					if isinstance(item[k], int) or isinstance(item[k], float):
						val = item[k]

					if date is not None and val is not None:
						break

				date_val[date] = val

			transformed_data.append({
				d['legend_label']: self.fill_missing_dates(date_val)
			})

		return transformed_data

	def save_output_data(self):
		output = self.transform_data()

		new_data = {}
		for item in output:
			k = list(item.keys())[0]

			vals = {}
			for key in item[k].keys():
				vals[datetime.datetime.strftime(key, '%Y-%m-%d')] = item[k][key]

			new_data[k] = vals
		output = new_data

		self.line_charts(list(output.values()), list(output.keys()), True)

		output = json.dumps(output)
		with open('./output/output.json', 'w') as outfile:
			json.dump(output, outfile)
