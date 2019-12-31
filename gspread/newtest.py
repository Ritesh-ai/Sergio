import os
import csv
import time
from Toolbox import Toolbox


def main():
    start = time.time()
    tlbx = Toolbox()
    sheet_name = "Some title here"

    workSheetNames = [i.split(".")[0] for i in os.listdir("files")]

    gsheet = tlbx.gsheet_new_sheet(sheet_name, workSheetNames, ['anubhadoriya1994@gmail.com'])
    gsheet_id = gsheet.id
    print(gsheet_id)

    # csvfile1 = "./files/csv1.csv"
    # tlbx.gsheet_upload_and_write_csv(gsheet, workSheetNames)

    # csvfile1 = "./files/csv1.csv"
    # tlbx.gsheet_upload_and_write_csv(gsheet, "Sheet1", csvfile1)

    # csvfile2 = "./files/csv2.csv"
    # tlbx.gsheet_upload_and_write_csv(gsheet, "Sheet2", csvfile2)

    # csvfile3 = "./files/csv3.csv"
    # tlbx.gsheet_upload_and_write_csv(gsheet, "Sheet3", csvfile3)

    end = time.time()
    print(end-start)
	
if __name__ == '__main__':
	main()
