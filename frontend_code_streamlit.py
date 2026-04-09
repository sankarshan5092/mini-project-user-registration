import streamlit as st
import mysql.connector
import bcrypt

# ---------------- DATABASE ----------------
connection_object = mysql.connector.connect(
    host=st.secrets["DB_HOST"],
    user=st.secrets["DB_USER"],
    password=st.secrets["DB_PASSWORD"],
    database=st.secrets["DB_NAME"],
    port=int(st.secrets["DB_PORT"])
)

cursor_object = connection_object.cursor()

# ---------------- PASSWORD FUNCTIONS ----------------
def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

# ---------------- BACKEND ----------------
def datainsert(full_name, address, ph_no, user_id, password):
    hashed_password = hash_password(password).decode("utf-8")

    sql = """
    INSERT INTO cust_details (full_name, address, ph_no, user_id, password)
    VALUES (%s, %s, %s, %s, %s)
    """

    data = (full_name, address, ph_no, user_id, hashed_password)

    try:
        cursor_object.execute(sql, data)
        connection_object.commit()
        return True
    except:
        connection_object.rollback()
        return False


def fetchdata(customer_login):
    query = "SELECT * FROM cust_details WHERE user_id = %s"
    cursor_object.execute(query, (customer_login,))
    return cursor_object.fetchone()


def fetchdata2(ph_no):
    query = "SELECT * FROM cust_details WHERE ph_no = %s"
    cursor_object.execute(query, (ph_no,))
    return cursor_object.fetchone()


def updatename(old_name, new_name):
    query = "UPDATE cust_details SET full_name = %s WHERE full_name = %s"
    cursor_object.execute(query, (new_name, old_name))
    connection_object.commit()


def deleterecord(user_id):
    query = "DELETE FROM cust_details WHERE user_id = %s"
    cursor_object.execute(query, (user_id,))
    connection_object.commit()


# ---------------- SESSION STATE ----------------
if "update_verified" not in st.session_state:
    st.session_state.update_verified = False
    st.session_state.old_name = ""

if "delete_verified" not in st.session_state:
    st.session_state.delete_verified = False
    st.session_state.delete_user = ""

# ---------------- UI ----------------
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

        elif len(ph_no) != 10 or not ph_no.isdigit():
            st.error("Invalid mobile number")

        elif fetchdata(user_id):
            st.error("User ID already exists")

        else:
            if datainsert(full_name, address, ph_no, user_id, password):
                st.success("Registration Successful")
            else:
                st.error("Registration Failed")

# ---------------- LOGIN ----------------
elif menu == "Existing User Login":
    st.header("Login")

    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        result = fetchdata(user_id)

        if result:
            if check_password(password, result[5]):
                st.success("Login Successful")

                st.write("### User Details")
                st.write(f"**Customer ID:** {result[0]}")
                st.write(f"**Name:** {result[1]}")
                st.write(f"**Address:** {result[2]}")
                st.write(f"**Mobile:** {result[3]}")
                st.write(f"**User ID:** {result[4]}")
                st.write(f"**Created Time:** {result[6]}")

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

        if result and check_password(password, result[5]):
            st.session_state.update_verified = True
            st.session_state.old_name = result[1]
            st.success("Login Successful")
        else:
            st.error("Invalid credentials")

    if st.session_state.update_verified:
        new_name = st.text_input("Enter New Name").upper().strip()

        if st.button("Update Name"):
            updatename(st.session_state.old_name, new_name)
            st.success("Name Updated Successfully")

            st.session_state.update_verified = False
            st.session_state.old_name = ""

# ---------------- DELETE ----------------
elif menu == "Delete Account":
    st.header("Delete Account")

    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Verify"):
        result = fetchdata(user_id)

        if result and check_password(password, result[5]):
            st.session_state.delete_verified = True
            st.session_state.delete_user = user_id
            st.success("Verification Successful")
        else:
            st.error("Invalid credentials")

    if st.session_state.delete_verified:
        confirm = st.radio("Confirm Delete?", ["No", "Yes"])

        if confirm == "Yes":
            if st.button("Delete Account Permanently"):
                deleterecord(st.session_state.delete_user)
                st.success("Account Deleted Successfully")

                st.session_state.delete_verified = False
                st.session_state.delete_user = ""