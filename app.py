import tkinter as tk
from tkinter import messagebox
import re
import mysql_connection_gui

mysql = mysql_connection_gui.Mysql()
mysql.start()

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

def is_valid_mobile(mobile):
    return mobile.isdigit() and len(mobile) == 10

def is_valid_roll(roll):
    a = []
    data = (mysql.display())
    for i in data:
        a.append(str(i[0]))
    return not (roll in a)

def is_valid_year(year):
    try:
        if len(year)!=4:
            return False
        year = int(year)
        return True
    except:
        return False

def add_data():
    name = name_entry.get()
    year = year_entry.get()
    rollno = rollno_entry.get()
    email = email_entry.get()
    mobile = mobile_entry.get()

    # Validation checks
    if not name or not year or not email or not mobile:
        messagebox.showerror("Input Error", "All fields must be filled out.")
        return
    
    if not is_valid_roll(rollno):
        messagebox.showerror("Input Error","Roll number already present.\nWant to update data?\nClick on UPDATE button.")
        return
    
    if not is_valid_year(year):
        messagebox.showerror("Input Error","Enter valid Year.")
        return
    
    if not is_valid_email(email):
        messagebox.showerror("Input Error", "Please enter a valid email address.")
        return
    
    if not is_valid_mobile(mobile):
        messagebox.showerror("Input Error", "Mobile number must be 10 digits long.")
        return
    
    messagebox.showinfo("Added Data", 
                        f"Name: {name}\nRoll No: {rollno}\nYear: {year}\nEmail: {email}\nMobile: {mobile}")
    mysql.insert(name,rollno,year,mobile,email)

    name_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    rollno_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    mobile_entry.delete(0, tk.END)

def display_data(arrange="id"):
    data = (mysql.display(arrange))
    box = tk.Tk()
    box.title("All Data")
    field = ["S. No.","Roll No.","Name","Year","Mobile Number","Email"]
    c = 0
    name_len = 5
    email_len = 20
    for i in data:
        name_len = max(name_len,len(i[1]))
        email_len = max(email_len,len(i[-1]))
    w = [7,10,name_len,5,12,email_len]
    for k in range(6):
        e = tk.Button(box,
                        text=field[k],
                        width=w[k],
                        fg='black',
                        font=('Arial',12,'bold'))
        e.grid(row=0,column=c)
        c += 1
    c = 1
    for i in range(len(data)):
        e = tk.Label(box,text=c,width=5,fg='grey',font=('Arial',10))
        e.grid(row=i+1,column=0)
        c += 1
        for j in range(len(data[i])):
            e = tk.Label(box,
                         text=data[i][j],
                        width=w[j+1],
                        fg='grey',
                        font=('Arial',10))
            e.grid(row=i+1, column=j+1)
    box.mainloop()

def update_data():
    name = name_entry.get()
    year = year_entry.get()
    rollno = rollno_entry.get()
    email = email_entry.get()
    mobile = mobile_entry.get()

    # Validation checks
    # if not name or not year or not email or not mobile:
    #     messagebox.showerror("Input Error", "All fields must be filled out.")
    #     return
    
    if not rollno:
        messagebox.showerror("Input Error","Enter roll number to update record.")
        return

    if is_valid_roll(rollno):
        messagebox.showerror("Input Error","Roll not present.\nClick on ADD data to add record.")
        return
    
    if not name and not year and not mobile and not email:
        messagebox.showerror("Input Error","Enter atleast one more field to update.")
        return
    
    if year:
        if not is_valid_year(year):
            messagebox.showerror("Input Error","Enter valid Year.")
            return
    
    if mobile:
        if not is_valid_mobile(mobile):
            messagebox.showerror("Input Error", "Mobile number must be 10 digits long.")
            return
    
    if email:
        if not is_valid_email(email):
            messagebox.showerror("Input Error", "Please enter a valid email address.")
            return
    
    if name:
        mysql.update("Name",name,"Id",rollno)
    if year:
        mysql.update("Year",year,"Id",rollno)
    if mobile:
        mysql.update("mob",mobile,"Id",rollno)
    if email:
        mysql.update("email",email,"Id",rollno)
    
    messagebox.showinfo("Data Updated", 
                        f"Name: {name}\nRoll No: {rollno}\nYear: {year}\nEmail: {email}\nMobile: {mobile}")

    name_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    rollno_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    mobile_entry.delete(0, tk.END)    

def delete_data():
    rollno = rollno_entry.get()
    if is_valid_roll(rollno):
        messagebox.showerror("Input Error","Enter valid roll number to delete data.")
        return
    a = messagebox.askquestion("Delete Data","Are you sure?")
    if a=="yes":
        mysql.delete(rollno)
    else:
        return
    rollno_entry.delete(0,tk.END)


app = tk.Tk()
app.title("Student Data Entry")

tk.Label(app, text="Name:",justify="left").grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(app)
name_entry.grid(row=0, column=1,columnspan=2, padx=10, pady=5)

tk.Label(app, text="Roll Number:",justify="left").grid(row=1, column=0, padx=10, pady=5)
rollno_entry = tk.Entry(app)
rollno_entry.grid(row=1, column=1,columnspan=2, padx=10, pady=5)

tk.Label(app, text="Year:",justify="left").grid(row=2, column=0, padx=10, pady=5)
year_entry = tk.Entry(app)
year_entry.grid(row=2, column=1,columnspan=2, padx=10, pady=5)

tk.Label(app, text="Email:").grid(row=3, column=0, padx=10, pady=5)
email_entry = tk.Entry(app)
email_entry.grid(row=3, column=1, columnspan=2,padx=10, pady=5)

tk.Label(app, text="Mobile No:").grid(row=4, column=0, padx=10, pady=5)
mobile_entry = tk.Entry(app)
mobile_entry.grid(row=4, column=1, columnspan=2,padx=10, pady=5)

add_button = tk.Button(app, text="Add Data", command=add_data)
add_button.grid(row=5, column=0, pady=20)
display_button = tk.Button(app,text="Display All Data",command=display_data)
display_button.grid(row=5,column=1,pady=20)
delete_button = tk.Button(app,text="Delete Data",command=delete_data)
delete_button.grid(row=6,column=0,pady=20)
update_button = tk.Button(app,text="Update Data",command=update_data)
update_button.grid(row=6,column=1,pady=20)

app.mainloop()
