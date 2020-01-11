from Toolbox import Toolbox
import csv
import os

# for i in os.listdir("files"):
#     print(i)


def main():
    tlbx = Toolbox()
    sheet_name = "Csv Collection"

    workSheetNames = [i.split(".")[0] for i in os.listdir("data")]
    
    gsheet = tlbx.gsheet_new_sheet(sheet_name, workSheetNames, ['rsengar7@gmail.com'])
    gsheet_id = gsheet.id
    print(gsheet_id)

    worksheet_list = gsheet.worksheets()
    print(worksheet_list)

    # for sheet in workSheetNames:
    #     csvfile = "./files/"+str(sheet)+".csv"
    #     print(csvfile)
    #     tlbx.gsheet_upload_and_write_csv(gsheet, sheet, csvfile)
    #     break
    
    """
    Returns the sh Object while calling and updating the csv files using gsheet_upload_and_write_csv
    """
    
    # csvfile1 = "./files/csv1.csv"
    # tlbx.gsheet_upload_and_write_csv(gsheet, "Sheet1", csvfile1)

    # csvfile2 = "./files/csv2.csv"
    # tlbx.gsheet_upload_and_write_csv(gsheet, "Sheet2", csvfile2)

    # csvfile3 = "./files/csv3.csv"
    # tlbx.gsheet_upload_and_write_csv(gsheet, "Sheet3", csvfile3)

	
if __name__ == '__main__':
	main()
