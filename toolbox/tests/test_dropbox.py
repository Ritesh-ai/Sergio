###	Import custom modules
import sys
sys.path.append('../')
from Toolbox import Toolbox
import datetime

def main():
	tlbx = Toolbox()
	confdict = {	
			"software_data":{
				"version":"1.0"
				, "name":"Test"
				, "log":"log_test"
			}
			, "mssql":{"host":""
				, "name":""
				, "user":""
				, "pass":""
			}
			, "dropbox":{"token":""}
		}

	tlbx.loadConfigFromVar(confdict)
	#result = tlbx.dropbox_store("C:\\Users\\admin\\Desktop\\dropbox-sdk-python-master\\tox.ini", "/Full_Share/")
	# result = tlbx.dropbox_list_files_iter("/Full_Share")
	# for row in result:
	# 	print(row.path_display)
	result = tlbx.dropbox_delete_outdated("/Full_Share", 30)


if __name__ == '__main__':
	main()