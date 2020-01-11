###	Import custom modules
import sys
sys.path.append('../')
from Toolbox import Toolbox

def main():
	tlbx = Toolbox()
	confdict = {	
			"software_data":{
				"version":"1.0"
				, "name":"Test"
				, "log":"log_test"
			}
			, "mssql":{"host":"108.46.153.144"
				, "name":"demo"
				, "user":"hlx"
				, "pass":"Devpass88"
			}
		}
	tlbx.loadConfigFromVar(confdict)
	tlbx.establish_MSSQLDict()	
	sql_query = """Select 'Test' AS [Data]"""
	tlbx.MSSQL_CURDict.execute(sql_query)
	result = tlbx.MSSQL_CURDict.fetchall()
	print(result)
	tlbx.MSSQL_CONNDict.close()

if __name__ == '__main__':
	main()
