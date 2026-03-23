import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")
url = f"{SERVER_URL}/getplan"

st.set_page_config(
    page_title="Fitness Plan Generator", page_icon=":muscle:", layout="centered"
)
st.title("Fitness Plan Generator")
st.write("Enter your details to get a personalized fitness plan.")


with st.form("input form"):
    qry = st.text_input("priority(upper body, lower body, full body): ")
    name = st.text_input("Name: ")
    age = st.text_input("Age: ")
    gender = st.text_area("Gender: ")
    goal = st.text_input("Goal: ")
    equipment = st.text_area("Equipment: ")
    weight = st.text_input("Weight(kg): ")
    illnesses = st.text_area("Illnesses: ")

    submit = st.form_submit_button("Submit")

if submit:
    if st.form is not None:
        data = {
            "qry": qry,
            "name": name,
            "age": age,
            "gender": gender,
            "goal": goal,
            "equipment": equipment,
            "weight": weight,
            "illnesses": illnesses,
        }
        response = requests.get(url, params=data)
        if response.status_code == 200:
            st.success("Data submitted successfully!")

            for key, value in response.json().items():
                st.write(f"{key}: {value}")
        else:
            st.error("Failed to submit data.")
    else:
        st.error("Please fill all the fields")
