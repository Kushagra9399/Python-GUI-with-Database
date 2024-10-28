class Queries:
    insert_query = "INSERT INTO trail (id, name, year, mob, email) VALUES (%s, %s, %s, %s, %s)"
    count = "SELECT COUNT(*) FROM trail"

    def select_all(self,arrange='id'):
        return f"SELECT * FROM trail ORDER BY {arrange}"

    def delete_query(self,a,b):
        b = self.convert(b)
        self.delete = f"DELETE FROM trail WHERE {a}={b}"
        return self.delete

    def convert(self,a):
        if type(a)==int:
            return a
        else:
            return "'"+a+"'"

    def update_query(self,a,b,c=0,d=0):
        b = self.convert(b)
        if c!=0:
            d = self.convert(d)
            self.update = f"UPDATE trail SET {a} = {b} WHERE {c}={d}"
        else:
            self.update = f"UPDATE trail SET {a}={b}"
        return self.update