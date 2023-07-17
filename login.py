import streamlit as st
import hashlib
import mysql.connector
import time

mydb=mysql.connector.connect(host=st.secrets['localhost'], user=st.secrets['root'], password=st.secrets['passw'], database=st.secrets['db'])
mycursor = mydb.cursor()

# mycursor.execute("Create Database if not exists webapp")
mycursor.execute(f"Use {db}")
mycursor.execute("Create table if not exists login  (username varchar(50) , email varchar(30), password varchar(200))")


st.set_page_config(
    page_title="Login Page",
    page_icon="🔏",
)

if "user_login" not in st.session_state:
    st.session_state['user_login'] = False


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

if "login" not in st.session_state:
    st.session_state["login"] = ""

if st.session_state['user_login'] == False:
    st.title("welcome! ")
    menu = ["Login", "SignUp"]
    choice = st.selectbox("Select Login or SignUp from dropdown box ▾", menu,)
    st.markdown("<h10 style='text-align: left; color: #ffffff;'> If you do not have an account, create an accouunt by select SignUp option from above dropdown box.</h10>",unsafe_allow_html=True)

    if choice == "":
            st.subheader("Login")
    elif choice == 'Login':
        st.write('-------')
        st.subheader('Log in to the App')
        email = st.text_input("Email", placeholder='email')
        password = st.text_input("Password", type='password')

        if st.checkbox("Login"):
            # if password == '12345':
            # Hash password creation and store in a table
            # create_usertable()
            hashed_pswd = make_hashes(password)


            mycursor.execute("Select * from login where email =%s and password = %s",(email, check_hashes(password, hashed_pswd)))
            # mycursor.execute("Select * from login where email =%s and password = %s",(str(email), str(password)))
            result = mycursor.fetchone()

            if result is not None:
                st.success("Successfully Logged in")
                if st.success:
                    st.session_state['user_login'] = True
                    st.experimental_rerun()
            else:
                st.warning("Incorrect Username / Password")
    elif choice == "SignUp":

        st.write('-----')
        st.subheader("Create New Account")
        new_user = st.text_input("Username", placeholder='name')
        new_user_email = st.text_input('Email id', placeholder='email')
        new_password = st.text_input("Password", type='password')
        if st.button("Signup"):

            if new_user == '':     # if user name empty then show the warnings
                st.warning('Invalid User name')
            elif new_user_email == '':   # if email empty then show the warnings
                st.warning('Invalid Email id')
            elif new_password == '':   # if password empty then show the warnings
                st.warning('Invalid Password')
            else:
                mycursor.execute("Select * from login where email =%s", (str(new_user_email),))
                res = mycursor.fetchone()

                if res is None :
                    mycursor.execute("Insert Into login values(%s, %s, %s)",(new_user, new_user_email, make_hashes(new_password)))
                    mydb.commit()
                    st.success("You have successfully created a valid Account")
                    st.info("Go up and Login to you account")
                else:
                    st.warning('Email is already registered')
                    st.info("Go up and Login to you account")
    elif choice == "Logout":
        st.session_state['user_login'] = False
        st.success("Bye . . .")
else:
    st.title("Do you want to Logout ?")
    menu = [" ","Login to another Account","Logout"]
    choice = st.selectbox("Select Logout or Another Login from dropdown box ▾", menu, )

    if choice == "":
        st.subheader("Logout. . . .")
    elif choice == "Logout":
        st.session_state['user_login'] = False
        st.success("Leaving So Soon ?\nBye . . .")
        time.sleep(1)
        st.experimental_rerun()
    elif choice == "Login to another Account":
        st.write('-------')
        st.subheader('Log in with another account')
        email = st.text_input("Email", placeholder='email')
        password = st.text_input("Password", type='password')

        if st.checkbox("Login"):
            # if password == '12345':
            # Hash password creation and store in a table
            # create_usertable()
            hashed_pswd = make_hashes(password)

            mycursor.execute("Select * from login where email =%s and password = %s",
                             (email, check_hashes(password, hashed_pswd)))
            # mycursor.execute("Select * from login where email =%s and password = %s",(str(email), str(password)))
            result = mycursor.fetchone()

            if result is not None:
                st.success("Successfully Logged in")
                if st.success:
                    st.session_state['user_login'] = True
                    st.experimental_rerun()
            else:
                st.warning("Incorrect Username / Password")
    else:
        pass





# if "my_input" not in st.session_state:
#     st.session_state['my_input'] = ""
#
# my_input = st.text_input("Input a text here",st.session_state['my_input'])
# submit = st.button("submit")
#
# if submit:
#     st.session_state['my_input'] = my_input
#     st.write(f"you typed {st.session_state['my_input']}")
