import os
import pandas as pd
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# Lets take the API key from environment variable
gemini_api_key = os.getenv("Gemini-API-Key1")

# Lets configure the model

model = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash-lite',
    api_key = gemini_api_key
)

# Designing the UI of application
st.title(':orange[Healthify:] :blue[Your Personal Health Assistant]')
st.markdown('''
This application will assist you to get better and customized health advice 
you can ask your health related issues and get personalized guidance.
            ''')

tips = '''
* Enter your details in the sidebar.
* Rate your activity and fitness level on a scale of 0-5.
* Submit your details.
* Ask your Question on the main page.
* Click on Generate and relax.
'''
st.write(f':green[**Tips to use this application:**] {tips}')

# Design the sidebar for all the user parameters
st.sidebar.header(':red[ENTER YOU DETAILS]')
Name = st.sidebar.text_input('Enter Your Name')
Gender = st.sidebar.selectbox('Select Your Gender',['Male','Female'])
Age = st.sidebar.text_input('Enter Your Age')
Weight = st.sidebar.text_input('Enter Your Weight (in kgs)')
Height = st.sidebar.text_input('Enter Your Height (in cms)')
BMI  = pd.to_numeric(Weight) / ((pd.to_numeric(Height)/100) ** 2)
Active = st.sidebar.slider('Rate your activity level (0-5)',0,5,step=1)
Fitness = st.sidebar.slider('Rate your fitness level (0-5)',0,5,step=1)
if st.sidebar.button('Submit'):
    st.sidebar.write(f"{Name}, Your BMI is {BMI:.2f} Kg/m²")

# Lets use Gemini model to generate the report
user_input = st.text_input('Ask me your questions related to health and fitness')
prompt = f'''
<Role> You are a health and fitness expert and 10+ year experience in guiding people with their health and fitness goals.
<Goal> Generate customized report addressing the problem the user is asked.
Here the queestion that user has asked :{user_input}.
<Context> Here are the details that user has provided:
Name: {Name}
Age: {Age}
Height: {Height}
Weight: {Weight}
Gender : {Gender}
BMI: {BMI:.2f} Kg/m²
Activity Rating (0-5): {Active}
Fitness Rating (0-5): {Fitness}
<format> Following should be outline of the report, in the sequence mentioned below:
* Start with 2-3 line of comment on details provided by user.
* Explain what thew real problem could be on the basis of input provided by user.
* Suggest the possible reasons for the problem. 
* What are the possible solutions.
* Mention the doctor from which specialization can be visited if required. 
* Mention any Changes in the diet which is required. 
* In last create a finnal summary of all the things that has be discussed in the report. 

<Instructions> 
* Use bullet points wherever required.
* Create tables to represent any data wherever required.
* Strictly do not advice any medicines.

'''

if st.button('Generate'):
    response = model.invoke(prompt)
    st.write(response.content)