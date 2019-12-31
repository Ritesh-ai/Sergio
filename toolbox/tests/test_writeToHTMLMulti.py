import sys
import os
import pandas as pd
sys.path.append('../')
from Toolbox import Toolbox


def main():
    tlbx = Toolbox()

    listXLTabs = []
    for file in os.listdir('/home/ritesh/Pictures/project/toolbox/data'):
        if file.split('.')[1] == "xlsx":
	        df = pd.read_excel('/home/ritesh/Pictures/project/toolbox/data/'+str(file))
        elif file.split('.')[1] == "csv":
	        df = pd.read_csv('/home/ritesh/Pictures/project/toolbox/data/'+str(file), encoding = "ISO-8859-1")
		
        dict1 = {'report_name':file.split(".")[0], 'report_result':df.to_dict(orient='records'),'indexState': df.to_dict(orient='records')[0].keys()}
        listXLTabs.append(dict1)
    
    # listXLTabs = [{
	# 				'report_name':'Sheet name'
	# 				, 'report_result':[{'Company Name': 'Amazon', 'Buyer': 'Hair dryer', 'ProductID': 'HAIR23143AM'}
	# 				, {'Company Name': 'Google', 'Buyer': 'AI', 'ProductID': 'AIGOO343'}
	# 				, {'Company Name': 'Alibaba', 'Buyer': 'Cosmatics', 'ProductID': 'POOROY2N4KIT2222'}]
	# 				, 'indexState': ['Company Name', 'Buyer', 'ProductID']
	# 			}
    #             ,{
	# 				'report_name':'Another Sheet'
	# 				, 'report_result':[{'Owner': 'Pogo', 'Buyer': 'Disney', 'Show': 'Road Runner'}
	# 				,{'Owner': 'Disney', 'Buyer': 'Cartoon Network', 'Show': 'Naruto'}
	# 				,{'Owner': 'Hungama', 'Buyer': 'Fun', 'Show': 'Dragon Ball Super'}]
	# 				, 'indexState': ['Owner', 'Buyer', 'Show']
	# 			},{
	# 				'report_name':'Yet another Sheet'
	# 				, 'report_result':[{'Company Name': 'Amazon', 'Buyer': 'Hair dryer', 'ProductID': 'HAIR23143AM'}
	# 				, {'Company Name': 'Google', 'Buyer': 'AI', 'ProductID': 'AIGOO343'}
	# 				, {'Company Name': 'Alibaba', 'Buyer': 'Cosmatics', 'ProductID': 'POOROY2N4KIT2222'}]
	# 				, 'indexState': ['Company Name', 'Buyer', 'ProductID']
	# 			}
    #             ]
	


	# Templates Options : BuildHTML, BuildHTMLFancy, buildHTMLFancyResponstable, sortable
    htmlresult = tlbx.writeToHTMLMulti(listXLTabs, template = 'BuildHTMLFancy')

    print(htmlresult)

if __name__ == '__main__':
	main()