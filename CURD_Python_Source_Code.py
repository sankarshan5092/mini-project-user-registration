#This is a new comment added 22/03/2026 21:17 IST
import mysql.connector #mysql=Module,connector=Class Name
connection_object=mysql.connector.connect(host="localhost",user="root",password="Sankarshan@1997",database="curd_nov_2025_mini_project_db")
cursor_object=connection_object.cursor()
#Creating a function for inserting data
def datainsert(full_name,address,ph_no,user_id,password):
    sql="insert into cust_details (full_name,address,ph_no,user_id,password) values (%s,%s,%s,%s,%s)"
    data=(full_name,address,ph_no,user_id,password)
    try:
        cursor_object.execute(sql,data)
        print ("REGISTRATION IS SUCCESSFUL")
        connection_object.commit()
    except mysql.connector.Error as e:
        print ("Error inserting data into table",e)
        connection_object.rollback()

#Taking input from the customer for new user creation
def newusercreation():
    full_name=input("Please enter your full name->").upper().strip()
    address=input("Please enter your address->").upper().strip()
    while True:
        ph_no = input("Please enter your mobile number->")
        result_from_db = fetchdata2(ph_no)
        if result_from_db:
            print ("This mobile number is already registered,please enter a different mobile number")
        elif len(ph_no)==10:
            break
        else:
            print ("Mobile number is invalid,it must be 10 digits long.Please enter correct mobile number")
    while True:
        user_id = input("Please enter your user ID->")
        result_from_db = fetchdata(user_id)
        if result_from_db:
            print("Sorry this user ID has already been taken please choose a different one")
        else:
            password = input("Please enter your password->")
            datainsert(full_name, address, ph_no, user_id, password)
            break

#Creating a function to fetch result from database by user_id
def fetchdata(customer_login):
    query=f"select * from cust_details where user_id=\'{customer_login}\'"
    try:
        cursor_object.execute(query)
        result = cursor_object.fetchone()
        return result
    except mysql.connector.Error as e:
        print ("Error fetching data from MySQL",e)
        connection_object.rollback()

#Creating a function to fetch result from database by mobile number
def fetchdata2(ph_no):
    query=f"select * from cust_details where ph_no=\'{ph_no}\'"
    try:
        cursor_object.execute(query)
        result = cursor_object.fetchone()
        return result
    except mysql.connector.Error as e:
        print ("Error fetching data from MySQL",e)
        connection_object.rollback()

#Creating functions to update details
def updatename(full_name,new_full_name):
    query=f"update cust_details set full_name=\'{new_full_name}\' where full_name=\'{full_name}\'"
    try:
        cursor_object.execute(query)
        #result = cursor_object.fetchone()
        connection_object.commit()
        #return result
    except mysql.connector.Error as e:
        print ("Error updating data in MySQL",e)
        connection_object.rollback()

#Creating a function to delete user record
def deleterecord(user_id):
    query=f"delete from cust_details where user_id=\'{user_id}\'"
    try:
        cursor_object.execute(query)
        print("RECORD HAS BEEN DELETED SUCCESSFULLY")
        connection_object.commit()
    except mysql.connector.Error as e:
        print ("Error deleting data from MySQL",e)
        connection_object.rollback()

#Main logic of the program
print ("Welcome to demo login application!!")
print ("1.New User Registration\n2.Existing User Login\n3.Update Details\n4.Delete Account")
response=input("Please select your choice->")
if response=="1":
    newusercreation()

elif response=="2":
    customer_login=input("Please enter your user ID->")
    result_from_db=fetchdata(customer_login)
    if result_from_db:
        customer_password=input("Please enter your password->")
        if customer_password==result_from_db[5]:
            print ("Congratulations you have successfully logged in please check your details")
            list_label=["Customer ID->","Name->","Address->","Mobile Number->","User ID->","Password->","User Created Date/Time->"]
            list_value=list(result_from_db)
            for list_label,list_value in zip(list_label,list_value):
                print (list_label,list_value)
        else:
            print ("Sorry you have entered wrong user ID or password please try again")
    else:
        print ("Sorry this user is not registered, you need to register yourself first")

elif response=="3":
    customer_login = input("Please enter your user ID->")
    result_from_db = fetchdata(customer_login)
    if result_from_db:
        customer_password = input("Please enter your password->")
        if customer_password == result_from_db[5]:
            print("Congratulations you have successfully logged in please check your details")
            list_label = ["Customer ID->", "Name->", "Address->", "Mobile Number->", "User ID->", "Password->","User Created Date/Time->"]
            list_value = list(result_from_db)
            for list_label,list_value in zip(list_label,list_value):
                print (list_label,list_value)
            res=input("Please type 1 to update your name->")
            if res=="1":
                full_name = input("Please enter your old full name->").upper().strip()
                new_full_name=input("Please enter your corrected name/new full name->").strip().upper()
                updatename(full_name, new_full_name)
                result_from_db = fetchdata(customer_login)
                list_label = ["Customer ID->", "Name->", "Address->", "Mobile Number->", "User ID->", "Password->","User Created Date/Time->"]
                list_value = list(result_from_db)
                for list_label, list_value in zip(list_label, list_value):
                    print(list_label, list_value)
        else:
            print("Sorry you have entered wrong password please try again")
    else:
        print("Sorry this user is not registered, you need to register yourself first")

elif response=="4":
    customer_login=input("Please enter the user ID for which you want to delete account->>")
    result_from_db = fetchdata(customer_login)
    if result_from_db:
        customer_password = input("Please enter your password for verification purpose->")
        if customer_password == result_from_db[5]:
            confirmation=input("Are you sure you want to delete your account ? Press Y to confirm else press N to retain your account->").strip().upper()
            if confirmation=="Y":
                deleterecord(customer_login)
            else:
                print ("Your account has been retained!!You can re-login to continue working with your account")
        else:
            print("Sorry you have entered wrong user ID or password please try again")

    else:
        print("Sorry this user is not registered hence cannot be deleted")
else:
    print ("Wrong choice please select options from 1 to 4")

connection_object.close()

#This code has been updated by Sankarshan


