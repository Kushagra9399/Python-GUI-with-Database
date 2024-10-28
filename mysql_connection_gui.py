import mysql.connector
import GUI_query

class Mysql:
    queries = GUI_query.Queries()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="kush",
        database= "kp"
    )
    def start(self):
        self.mycur = self.mydb.cursor()
        self.mycur.execute("set sql_safe_updates=0")
    
    def close(self):
        self.mycur.execute("set sql_safe_updates=1")
        self.mydb.close()
    
    def insert(self,name,rollno,year,mob,email):
        val = (rollno,name,year,mob,email)
        ins = self.queries.insert_query
        self.mycur.execute(ins,val)
        self.mydb.commit()

    def count(self):
        self.mycur.execute("SELECT COUNT(*) FROM TRAIL")
        id = self.mycur.fetchone()[0]
        return id
    
    def display(self,arrange="id"):
        dis = self.queries.select_all(arrange)
        self.mycur.execute(dis)
        data = self.mycur.fetchall()
        return data
    
    def update(self,change,set,change_condition=0,equal=0):
        try:
            qu = self.queries.update_query(change,set,change_condition,equal)
            self.mycur.execute(qu)
            self.mydb.commit()
            return True
        except Exception as e:
            print("na re")
            print(e)
            return False
    
    def delete(self,rollno):
        del_q = self.queries.delete_query("id",rollno)
        self.mycur.execute(del_q)
        self.mydb.commit()