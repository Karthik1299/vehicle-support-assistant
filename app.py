import streamlit as st
import requests

st.title("Vehicle Support Assistant")
st.write("Enter your vehicle issue (e.g., 'My car shows P0420' or 'Engine misfiring')")

# Input form
with st.form("query_form"):
    user_input = st.text_input("Describe the issue or enter an OBD code:")
    submitted = st.form_submit_button("Get Diagnosis")

if submitted and user_input:
    # Call FastAPI backend
    try:
        response = requests.post("http://127.0.0.1:8000/diagnose", json={"text": user_input})
        diagnosis = response.json()["diagnosis"]
        st.success("Diagnosis:")
        st.write(diagnosis)
    except Exception as e:
        st.error(f"Error: {str(e)}")