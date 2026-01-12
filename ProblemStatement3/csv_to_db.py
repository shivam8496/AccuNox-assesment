import sqlite3
import csv
import os
import traceback
class GenrateDatabase:
    def __init__(self,csv_path="sample_data.csv",db_path="csv_to_database.db"):
        self.db = self.init_db(db_path=db_path)
        self.csv_path = csv_path

    def init_db(self,db_path):
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS departments(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        department TEXT UNIQUE
                        )
                        ''')
            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS address (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        street TEXT ,
                        pincode INTEGER,
                        UNIQUE(street , pincode)
                        )
                        ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS employee (
                        id INTEGER PRIMARY KEY AUTOINCREMENT ,
                        email TEXT UNIQUE , 
                        name TEXT ,
                        role TEXT ,
                        dept_id INTEGER , 
                        addr_id INTEGER , 
                        FOREIGN KEY (dept_id) REFERENCES departments (id),
                        FOREIGN KEY (addr_id) REFERENCES address (id)
                        )
                        ''')
            connection.commit()
            return connection
        except Exception as e:
            print(f"[init_db]:Error -> {e}")
            return None


    def _create_insert_address(self,cursor,street,pincode):
        try:   
            cursor.execute("SELECT id from address where street = ? AND pincode = ?",(street,pincode))
            res = cursor.fetchone()
            if res:
                return res[0]
            cursor.execute("INSERT INTO address (street , pincode) VALUES (?,?) ",(street,pincode))
            return cursor.lastrowid
        except Exception as e:
            print(f"[_create_insert_address]:ERROR -> {e }")
            return None
        
    def _create_insert_department(self,cursor,department):
        try:
            cursor.execute("SELECT id from departments where department = ?",(department,))
            res = cursor.fetchone()
            if res:
                return res[0]
            cursor.execute("INSERT INTO departments (department) VALUES (?) ",(department,))
            return cursor.lastrowid
        except Exception as e:
            print(f"[_create_insert_department]:ERROR -> {e }")
            return None
        

    def _process_large_db(self):
        try:
            with open(self.csv_path , 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    yield row
        except Exception as e:
            print("[_process_large_db]:ERROR",e)

    def save_to_db(self,batch=1000):
        cursor = self.db.cursor()
        counter=0
        pending_changes = False
        try:
            for row in self._process_large_db():
                dept_id = self._create_insert_department(cursor,row["department"])
                addr_id= self._create_insert_address(cursor,row["street"],row["pincode"])

                query = '''
                    INSERT INTO  employee (name,email,role,dept_id,addr_id) 
                    VALUES (?,?,?,?,?)
                    ON CONFLICT(email) DO UPDATE SET
                            name = excluded.name,
                            role = excluded.role,
                            dept_id = excluded.dept_id,
                            addr_id = excluded.addr_id;
                        '''
                cursor.execute(query,(row['name'],row['email'],row['role'],dept_id,addr_id))
                counter+=1
                pending_changes = True
                if counter%batch==0:
                    pending_changes = False
                    print(f"Processed {counter} calls ... Commiting data!!")
                    self.db.commit()
            
            if pending_changes:
                print("Commiting remaining Changes ..........")
                self.db.commit()
            print("DataBase Saved ..... ")
        
        except Exception as e:
            traceback.print_exc()
            print(f"[save_to_db]:Error Occurred {e}")
            
if __name__=="__main__":
    save = GenrateDatabase()
    save.save_to_db(1000)