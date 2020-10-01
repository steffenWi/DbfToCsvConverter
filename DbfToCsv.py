from dbfread import DBF
import glob
import sys
import os
import csv


def LoadDbfFile(file):
    dbfTable = DBF(file, load=True, encoding="cp437")
    return dbfTable


def WriteCsvFile(filepath, filecontent):
    try:
        writer = csv.writer(open(filepath, "x", newline=''), delimiter=sys.argv[3], quoting=csv.QUOTE_NONE, escapechar='\\')
        writer.writerows(filecontent)
    except Exception as ex:
        print(filepath+":")
        print(ex)
    return

def ConvertDbfToCsv(dbfContent):
    try:
        csvlines = []
        csvlines.append(dbfContent.field_names)
        for dbfRecord in dbfContent.records:
            csvlines.append(list(str(convstr) for convstr in dbfRecord.values()))
    except TypeError as te:
        print(te)
    return csvlines


try:
    if (len(sys.argv) != 4):
        print("The following parameters are required:\r\n\t1. Directory to read\r\n\t2. Directory to write CSV files to\r\n\t3. CSV delimiter"
              +"\r\nExample: DbfToCsv.py \"/home/user name/DBF\" \"/home/username/CSV\" \";\"")
        exit(-1)

    if (os.path.exists(sys.argv[1]) == False):
        print("The path to the DBF folder does not exist or you do not have permission to access it.")
        exit(-1)
    elif(os.path.exists(sys.argv[2]) == False):
        print("The path to the CSV folder does not exist or you do not have permission to access it.")
        exit(-1)

    dbfFiles = glob.glob(os.path.join(sys.argv[1], "*.DBF"))
    for dbffile in dbfFiles:
        convertedDbfContent = LoadDbfFile(dbffile)
        text = ConvertDbfToCsv(convertedDbfContent)
        csvname = os.path.basename(dbffile)
        csvname = os.path.splitext(csvname)[0]
        csvfilepath = os.path.join(sys.argv[2], csvname + ".csv")
        WriteCsvFile(csvfilepath, text)
except Exception as ex:
    print(ex)
