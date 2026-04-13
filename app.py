import streamlit as st

st.title("Login/Register")
name = st.text_input("Enter your name: ")
#age = int(st.number_input("Enter your age",0,120,25,1))
age = st.text_input("Enter your age: ")
if age:
    age = int(age)
status = st.radio("Select gender: ",['Male','Female'])

#if status == 'Male':
    #st.success("Male")
#else:
    #st.success("Female")

email = st.text_input("Enter your email")
if st.button("Submit"):
    result = "Login Successful !!"
    st.success(result)