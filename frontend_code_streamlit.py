import streamlit as st
import mysql.connector

# ---------------- DATABASE ----------------
connection_object = mysql.connector.connect(
    host=st.secrets["DB_HOST"],
    user=st.secrets["DB_USER"],
    password=st.secrets["DB_PASSWORD"],
    database=st.secrets["DB_NAME"],
    port=int(st.secrets["DB_PORT"])
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

# ---------------- STREAMLIT UI ----------------

st.title("Customer Management System")

menu = st.sidebar.selectbox(
    "Select Option",
    ["New User Registration", "Existing User Login", "Update Details", "Delete Account"]
)

# ---------------- REGISTER ----------------
if menu == "New User Registration":
    st.header("Register New User")

    full_name = st.text_input("Full Name").upper().strip()
    address = st.text_input("Address").upper().strip()
    ph_no = st.text_input("Mobile Number")
    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if fetchdata2(ph_no):
            st.error("Mobile number already exists")
        elif len(ph_no) != 10:
            st.error("Invalid mobile number")
        elif fetchdata(user_id):
            st.error("User ID already exists")
        else:
            if datainsert(full_name,address,ph_no,user_id,password):
                st.success("Registration Successful")

# ---------------- LOGIN ----------------
elif menu == "Existing User Login":
    st.header("Login")

    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        result = fetchdata(user_id)

        if result:
            if password == result[5]:
                st.success("Login Successful")

                st.write("### User Details")
                labels = ["Customer ID","Name","Address","Mobile","User ID","Password","Created Time"]
                for l,v in zip(labels,result):
                    st.write(f"**{l}:** {v}")
            else:
                st.error("Wrong password")
        else:
            st.error("User not registered")

# ---------------- UPDATE ----------------
elif menu == "Update Details":
    st.header("Update Name")

    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login to Update"):
        result = fetchdata(user_id)

        if result and password == result[5]:
            st.success("Login Successful")

            new_name = st.text_input("Enter New Name").upper().strip()

            if st.button("Update Name"):
                old_name = result[1]
                updatename(old_name, new_name)
                st.success("Name Updated Successfully")
        else:
            st.error("Invalid credentials")

# ---------------- DELETE ----------------
elif menu == "Delete Account":
    st.header("Delete Account")

    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Verify"):
        result = fetchdata(user_id)

        if result and password == result[5]:
            confirm = st.radio("Confirm Delete?", ["No", "Yes"])

            if confirm == "Yes":
                deleterecord(user_id)
                st.success("Account Deleted Successfully")
        else:
            st.error("Invalid credentials")

# ---------------- CLOSE DB ----------------
# (Streamlit auto reruns, so no manual close needed)