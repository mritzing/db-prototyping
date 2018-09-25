from collections import Counter
from .database.dbTools import connectDB
import os
import io
import datetime

from threading import Thread
import functools

def timeout(seconds_before_timeout):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, seconds_before_timeout))]
            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e
            t = Thread(target=newFunc)
            t.daemon = True
            try:
                t.start()
                t.join(seconds_before_timeout)
            except Exception as e:
                print('error starting thread')
                raise e
            ret = res[0]
            if isinstance(ret, BaseException):
                print("moving on")
            return ret
        return wrapper
    return deco

class Parser:

    def __init__(self):
        self.totals = Counter()
        self.conn = connectDB()
        self.cur = self.conn.cursor()
        self.uploadDir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'static', 'uploads'))
    ### SQL Insertion Blocks ###
    # In the future SQLalchemy can be used to create wrapper methods to generate these
    #  kinds of commands but for now it is good for me to relearn
    # http://initd.org/psycopg/docs/usage.html

    compoundSQL = "INSERT INTO compound (notation) VALUES(%s) RETURNING compound_id;"
    compound_infoSQL = """INSERT INTO compound_info (compound_id, name, author, dateCreated, theoretical_mass, scientific_mass, time_passed)
                    VALUES(%s,%s,%s,%s,%s,%s,%s) """
    storageSQL = "INSERT INTO storage (compound_id, file_loc) VALUES(%s, %s) "
    atom_infoSQL = "INSERT INTO atom_info (compound_id, molecule_id, atom_type, x_coord, y_coord, z_coord) VALUES(%s,%s,%s,%s,%s,%s)"
    updatecompound= "UPDATE compound SET notation = %s WHERE compound_id = %s"
    


    def parseFile(self, contents, filename):
        #insert compound value  
        self.cur.execute(self.compoundSQL, (None,))
        idNum = self.cur.fetchone()[0]
        atomList = []
        compoundName = None
        ifStream = io.StringIO(contents.decode('utf-8'))
        writeFile = getattr(filename, 'filename', None)
        #with open(filename, 'r') as pdbFile:
            #for line in pdbFile.readlines():
        file = open(os.path.join(self.uploadDir, writeFile), 'w')

        for line in ifStream.readlines():
            file.write(line)
            lineArr = line.split()
            if lineArr[0] is "TERM":
                #breakout into ligand
                print('term')
            if lineArr[0] is "HETNAM":
                compoundName = lineArr[-1]
            if "HETAT" in lineArr[0] or "ATOM" in lineArr[0]:
                atomList.append([idNum, lineArr[1], lineArr[-1], lineArr[6], lineArr[7], lineArr[8],])
                #counts occurences
                self.totals[lineArr[-1]] += 1
    
        file.close()
        #fix compound value notation
        totalObj = self.molMass()
        self.cur.execute(self.updatecompound,(totalObj[0],idNum))
        self.cur.executemany(self.atom_infoSQL, atomList)
        self.cur.execute(self.storageSQL,(idNum,writeFile,))
        self.cur.execute(self.compound_infoSQL,(idNum, compoundName, "PDBDownload", datetime.datetime.now(),totalObj[1], None, None,))
        self.conn.commit()
        atomList.clear()
        self.totals.clear()
        return totalObj

    # Ex lines:
    # HETATM    3  NAQ DRG     1      18.720   7.260   1.360  1.00 20.00           N
    # HETATM    4  OAT DRG     1      20.090   7.560   1.340  1.00 20.00           O
    # Need more info on how to properly parse these
    # pbd reference: https://zhanglab.ccmb.med.umich.edu/COFACTOR/pdb_atom_format.html

    def returnAllRes(self):
        self.cur.execute("SELECT * FROM compound_info")
        print("executing fetch")
        return self.cur.fetchall();

    def molMass(self):
        totalMass = 0
        notation = ""
        for element in self.totals.keys():
            elementMass = self.atomic_mass[element]*self.totals[element]
            totalMass = totalMass + elementMass
            #notation string will be built here for now until i figure out the right way to do it
            notation = notation + element + str(self.totals[element])
        return [notation,totalMass]


    atomic_mass = {
        "H": 1.0079, "HE": 4.0026, "LI": 6.941, "BE": 9.0122,
        "B": 10.811, "C": 12.011, "N": 14.007, "O": 15.999, "F": 18.998,
        "NE": 20.180, "NA": 22.990, "MG": 24.305, "AL": 26.982,
        "SI": 28.086, "P": 30.974, "S": 32.065, "CL": 35.453,
        "AR": 39.948, "K": 39.098, "CA": 40.078, "SC": 44.956,
        "TI": 47.867, "V": 50.942, "CR": 51.996, "MN": 54.938,
        "FE": 55.845, "CO": 58.933, "NI": 58.693, "CU": 63.546,
        "ZN": 65.39, "GA": 69.723, "GE": 72.61, "AS": 74.922,
        "SE":78.96, "BR": 79.904, "KR": 83.80, "RB": 85.468, "SR": 87.62,
        "Y": 88.906, "ZR": 91.224, "NB": 92.906, "MO": 95.94,
        "TC": 97.61, "RU": 101.07, "RH": 102.91, "PD": 106.42,
        "AG": 107.87, "CD": 112.41, "IN": 114.82, "SN": 118.71,
        "SB": 121.76, "TE": 127.60, "I": 126.90, "XE": 131.29,
        "CS": 132.91, "BA": 137.33, "LA": 138.91, "CE": 140.12,
        "PR": 140.91, "ND": 144.24, "PM": 145.0, "SM": 150.36, "EU": 151.96,
        "GD": 157.25, "TB": 158.93, "DY": 162.50, "HO": 164.93, "ER": 167.26,
        "TM": 168.93, "YB": 173.04, "LU": 174.97, "HF": 178.49, "TA": 180.95,
        "W": 183.84, "RE": 186.21, "OS": 190.23, "IR": 192.22, "PT": 196.08,
        "AU": 196.08, "HG": 200.59, "TL": 204.38, "PB": 207.2, "BI": 208.98,
        "PO": 209.0, "AT": 210.0, "RN": 222.0, "FR": 223.0, "RA": 226.0,
        "AC": 227.0, "TH": 232.04, "PA": 231.04, "U": 238.03, "NP": 237.0,
        "PU": 244.0, "AM": 243.0, "CM": 247.0, "BK": 247.0, "CF": 251.0, "ES": 252.0,
        "FM": 257.0, "MD": 258.0, "NO": 259.0, "LR": 262.0, "RF": 261.0, "DB": 262.0,
        "SG": 266.0, "BH": 264.0, "HS": 269.0, "MT": 268.0
    }
