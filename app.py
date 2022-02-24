#import Modules
import os
import pyrebase
import streamlit as st
import numpy as np
from PIL import  Image
from datetime import datetime

# configuration key
firebaseConfig = {
    'apiKey': "AIzaSyDbDfr3QYJqN-BpgRtrfG_7euyRu6Joa2w",
    'authDomain': "quipit-45420.firebaseapp.com",
    'projectId': "quipit-45420",
    'databaseURL': "https://quipit-45420-default-rtdb.europe-west1.firebasedatabase.app/",
    'storageBucket': "quipit-45420.appspot.com",
    'messagingSenderId': "629651025885",
    'appId': "1:629651025885:web:e9978355fef64f12ad9034",
    'measurementId': "G-29827YJ860"
}

# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()
st.sidebar.title("Quipitapp")

# Authentication
choice = st.sidebar.selectbox('login/Signup', ['Login', 'Sign up'])

# Obtain User Input for email and password
email = st.sidebar.text_input('Please enter your email address')
password = st.sidebar.text_input('Please enter your password',type = 'password')

# App 

# Sign up Block
if choice == 'Sign up':
    handle = st.sidebar.text_input('Please input your app handle name', value='Default')
    submit = st.sidebar.button('Create my account')

    if submit:
        user = auth.create_user_with_email_and_password(email, password)
        st.success('Your account is created sucessfully!')
        st.balloons()
        # Sign in
        user = auth.sign_in_with_email_and_password(email, password)
        db.child(user['localId']).child("Handle").set(handle)
        db.child(user['localId']).child("ID").set(user['localId'])
        st.title('Welcome' + handle)
        st.info('Login via login drop down selection')

# Custom imports 
from multipage import MultiPage
from pages import data_upload, machine_learning, metadata, data_visualize, redundant # import your pages here

# Create an instance of the app 
app = MultiPage()

# Title of the main page
display = Image.open('Logo.png')
display = np.array(display)
# st.image(display, width = 400)
# st.title("Data Storyteller Application")
col1, col2 = st.beta_columns(2)
col1.image(display, width = 400)
col2.title("Data Storyteller Application")

# Add all your application here
app.add_page("Upload Data", data_upload.app)
app.add_page("Change Metadata", metadata.app)
app.add_page("Machine Learning", machine_learning.app)
app.add_page("Data Analysis",data_visualize.app)
app.add_page("Y-Parameter Optimization",redundant.app)

# The main app
app.run()
