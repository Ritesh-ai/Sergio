###	Import custom modules
import sys
sys.path.append('../')
from Toolbox import Toolbox
import datetime
################################################################################
######	A temporary space to create & test functions with SQL
################################################################################

def getPronumber(tlbx):
	tlbx.establish_MSSQLDict()
	#sql_query = """SELECT * FROM [ADS].[dbo].[tvfADS_CalculateKitPrice] ('RDX5M10')"""
	sql_query = """SELECT * FROM [ADS].[dbo].[tvfADS_CalculateKitPrice_group] ('RDX5M10')"""
	tlbx.MSSQL_CURDict.execute(sql_query)
	result = tlbx.MSSQL_CURDict.fetchall()
	print(result)
	# return_odoo_select = []
	# for row in result:
	# 	return_odoo_select.append((
	# 		row['PRONumber'].strip()
	# 		, row['PRONumber'].strip()
	# 		))
	# tlbx.MSSQL_CONNDict.close()
	# return return_odoo_select

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
		}

	tlbx.loadConfigFromVar(confdict)
	result = getPronumber(tlbx)
	print(result)

if __name__ == '__main__':
	main()
