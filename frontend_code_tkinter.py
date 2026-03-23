import mysql.connector
import tkinter as tk
from tkinter import messagebox

# ---------------- DATABASE ----------------
connection_object = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sankarshan@1997",
    database="curd_nov_2025_mini_project_db"
)
cursor_object = connection_object.cursor()

# ---------------- BACKEND (UNCHANGED) ----------------

def datainsert(full_name,address,ph_no,user_id,password):
    sql="insert into cust_details (full_name,address,ph_no,user_id,password) values (%s,%s,%s,%s,%s)"
    data=(full_name,address,ph_no,user_id,password)
    try:
        cursor_object.execute(sql,data)
        connection_object.commit()
        return True
    except:
        connection_object.rollback()
        return False

def fetchdata(customer_login):
    query=f"select * from cust_details where user_id='{customer_login}'"
    cursor_object.execute(query)
    return cursor_object.fetchone()

def fetchdata2(ph_no):
    query=f"select * from cust_details where ph_no='{ph_no}'"
    cursor_object.execute(query)
    return cursor_object.fetchone()

def updatename(full_name,new_full_name):
    query=f"update cust_details set full_name='{new_full_name}' where full_name='{full_name}'"
    cursor_object.execute(query)
    connection_object.commit()

def deleterecord(user_id):
    query=f"delete from cust_details where user_id='{user_id}'"
    cursor_object.execute(query)
    connection_object.commit()

# ---------------- FRONTEND FUNCTIONS ----------------

def register_user():
    full_name = entry_name.get().upper().strip()
    address = entry_address.get().upper().strip()
    ph_no = entry_phone.get()
    user_id = entry_userid.get()
    password = entry_password.get()

    if fetchdata2(ph_no):
        messagebox.showerror("Error", "Mobile number already exists")
    elif len(ph_no) != 10:
        messagebox.showerror("Error", "Invalid phone number")
    elif fetchdata(user_id):
        messagebox.showerror("Error", "User ID already exists")
    else:
        if datainsert(full_name,address,ph_no,user_id,password):
            messagebox.showinfo("Success", "Registration Successful")

def login_user():
    user_id = entry_login_user.get()
    password = entry_login_pass.get()

    result = fetchdata(user_id)

    if result:
        if password == result[5]:
            info = f"""
Customer ID: {result[0]}
Name: {result[1]}
Address: {result[2]}
Phone: {result[3]}
User ID: {result[4]}
"""
            messagebox.showinfo("Login Success", info)
        else:
            messagebox.showerror("Error", "Wrong password")
    else:
        messagebox.showerror("Error", "User not found")

def update_user():
    user_id = entry_login_user.get()
    password = entry_login_pass.get()
    new_name = entry_new_name.get().upper().strip()

    result = fetchdata(user_id)

    if result and password == result[5]:
        old_name = result[1]
        updatename(old_name, new_name)
        messagebox.showinfo("Success", "Name Updated")
    else:
        messagebox.showerror("Error", "Invalid credentials")

def delete_user():
    user_id = entry_login_user.get()
    password = entry_login_pass.get()

    result = fetchdata(user_id)

    if result and password == result[5]:
        confirm = messagebox.askyesno("Confirm", "Delete account?")
        if confirm:
            deleterecord(user_id)
            messagebox.showinfo("Deleted", "Account Deleted")
    else:
        messagebox.showerror("Error", "Invalid credentials")

# ---------------- UI ----------------

root = tk.Tk()
root.title("Customer Management System")
root.geometry("400x500")

# -------- REGISTER --------
tk.Label(root, text="Register", font=("Arial", 14)).pack(pady=5)

entry_name = tk.Entry(root)
entry_name.pack()
entry_name.insert(0, "Full Name")

entry_address = tk.Entry(root)
entry_address.pack()
entry_address.insert(0, "Address")

entry_phone = tk.Entry(root)
entry_phone.pack()
entry_phone.insert(0, "Phone")

entry_userid = tk.Entry(root)
entry_userid.pack()
entry_userid.insert(0, "User ID")

entry_password = tk.Entry(root)
entry_password.pack()
entry_password.insert(0, "Password")

tk.Button(root, text="Register", command=register_user).pack(pady=10)

# -------- LOGIN --------
tk.Label(root, text="Login", font=("Arial", 14)).pack(pady=5)

entry_login_user = tk.Entry(root)
entry_login_user.pack()
entry_login_user.insert(0, "User ID")

entry_login_pass = tk.Entry(root)
entry_login_pass.pack()
entry_login_pass.insert(0, "Password")

tk.Button(root, text="Login", command=login_user).pack(pady=5)

# -------- UPDATE --------
entry_new_name = tk.Entry(root)
entry_new_name.pack()
entry_new_name.insert(0, "New Name")

tk.Button(root, text="Update Name", command=update_user).pack(pady=5)

# -------- DELETE --------
tk.Button(root, text="Delete Account", command=delete_user).pack(pady=5)

root.mainloop()

connection_object.close()