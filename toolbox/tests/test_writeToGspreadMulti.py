import sys
import os
import pandas as pd
sys.path.append('../')
from Toolbox import Toolbox


def main():
    tlbx = Toolbox()
    sheet_title = "Csv Collection"
    listXLTabs = [{
					'report_name':'Sheet name'
					, 'report_result':[{'Company Name': 'Amazon', 'Buyer': 'Hair dryer', 'ProductID': 'HAIR23143AM'}
					, {'Company Name': 'Google', 'Buyer': 'AI', 'ProductID': 'AIGOO343'}
					, {'Company Name': 'Alibaba', 'Buyer': 'Cosmatics', 'ProductID': 'POOROY2N4KIT2222'}]
					, 'indexState': ['Company Name', 'Buyer', 'ProductID']
				}
                ,{
					'report_name':'Another Sheet'
					, 'report_result':[{'Owner': 'Pogo', 'Buyer': 'Disney', 'Show': 'Road Runner'}
					,{'Owner': 'Disney', 'Buyer': 'Cartoon Network', 'Show': 'Naruto'}
					,{'Owner': 'Hungama', 'Buyer': 'Fun', 'Show': 'Dragon Ball Super'}]
					, 'indexState': ['Owner', 'Buyer', 'Show']
				},{
					'report_name':'Yet another Sheet'
					, 'report_result':[{'Company Name': 'Amazon11', 'Buyer': 'Hair dryer', 'ProductID': 'HAIR23143AM'}
					, {'Company Name': 'Google', 'Buyer': 'AI', 'ProductID': 'AIGOO343'}
					, {'Company Name': 'Alibaba', 'Buyer': 'Cosmatics', 'ProductID': 'POOROY2N4KIT2222'}]
					, 'indexState': ['Company Name', 'Buyer', 'ProductID']
				}
                ]

	# Templates Options : BuildHTML, BuildHTMLFancy, buildHTMLFancyResponstable, sortable
    htmlresult = tlbx.writeToGspreadMulti(sheet_title, listXLTabs, gsheet_id=None, sharelist = ['itest4999@gmail.com'])

    print(htmlresult)

if __name__ == '__main__':
	main()