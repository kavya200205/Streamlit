import streamlit as st

st.title("Job Opportunity")
name = st.text_input("Enter your full name: ")
gender = st.radio("Enter your gender: ",['Male','Female'])
role = st.selectbox("Select the job role you want to choose",['Data Analyst','Programmer','Associate Engineer','Tester'])

image = st.file_uploader("Choose a jpg or jpeg file",type = 'jpeg/jpg')
st.write("Upload your image above")

resume = st.file_uploader("Upload your resume",type = 'pdf/doc')

number = st.text_input("Enter your number")

if st.button("Submit"):
    result = "Your details are saved and submitted successfully"
    res = "Thank you for applying in our company"
    st.success(result)
    st.info(res)
