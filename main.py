import streamlit as st
import pandas as pd
from report_utils import generate_pdf_report
from data_utils import read_csv
from email_utils import send_email  # Assuming you have this function in a module named `email_utils`

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "df" not in st.session_state:
    st.session_state.df = None
if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False
if "report_generated" not in st.session_state:
    st.session_state.report_generated = False
if "email_info" not in st.session_state:
    st.session_state.email_info = {
        "to_address": "",
        "subject": "Generated Report",
        "body": "Please find the attached report.",
        "send_now": True,
        "send_datetime": None,
    }

def send_message(content):
    st.session_state.chat_history.append({"role": "bot", "content": content})

def handle_bot_response(user_input):
    user_input = user_input.lower()
    if "generate report" in user_input:
        if st.session_state.df is not None:
            send_message("Generating report...")
        else:
            send_message("Please upload a CSV file first.")
    elif "upload csv" in user_input:
        send_message("Please upload a CSV file.")
    elif "send email" in user_input:
        send_message("Please fill the email deatils")
    else:
         send_message(
            "Hello! I'm here to help you with the following tasks:\n"
            "- Upload a CSV file: 'Upload CSV'\n"
            "- Generate a report: 'Generate Report'\n"
            "- Send the report via email: 'Send Email'\n"
            "How can I assist you today?"
        )

st.title("AI Conversational Bot")

def on_submit():
    prompt = st.session_state.input_field
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    handle_bot_response(prompt)
    st.session_state.input_field = ""

def ask_email_info():
    st.session_state.email_info["to_address"] = st.text_input("Recipient Email Address")
    st.session_state.email_info["subject"] = st.text_input("Email Subject", value="Generated Report")
    st.session_state.email_info["body"] = st.text_area("Email Body", value="Please find the attached report.")
    st.session_state.email_info["send_now"] = st.checkbox("Send now?", value=True)
    if not st.session_state.email_info["send_now"]:
        st.session_state.email_info["send_datetime"] = st.datetime_input("Schedule send time")

    if st.button("Send Email"):
        send_email(
            st.session_state.email_info["to_address"],
            st.session_state.email_info["subject"],
            st.session_state.email_info["body"],
            st.session_state.pdf_path,
            "report.pdf",
            st.session_state.email_info["send_datetime"] if not st.session_state.email_info["send_now"] else None
        )
        send_message("Email has been sent successfully.")

for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        with st.chat_message("user"):
            st.write(chat["content"])
    elif chat["role"] == "bot":
        with st.chat_message("assistant"):
            st.write(chat["content"])
        if chat["content"] == "Please upload a CSV file." and not st.session_state.uploaded:
            uploaded_file = st.file_uploader("Upload CSV file", type="csv", key="file_uploader")
            if uploaded_file is not None:
                st.session_state.df = read_csv(uploaded_file)
                st.session_state.uploaded = True
                send_message("CSV file uploaded successfully!")
                st.experimental_rerun()
        elif chat["content"] == "Generating report...":
            status = st.status("Generating report...", state="running")
            try:
                pdf_buffer, pdf_path = generate_pdf_report(st.session_state.df)
                st.session_state.pdf_path = pdf_path
                st.session_state.pdf_buffer = pdf_buffer
                st.session_state.report_generated = True
                status.update(label="Report generated successfully!", state="complete")
                with st.container():
                    st.download_button(
                        label="Download Report",
                        data=st.session_state.pdf_buffer,
                        file_name="report.pdf",
                        mime="application/pdf"
                    )
                    ask_email_info()
            except Exception as e:
                status.update(label="An error occurred while generating the report.", state="error")
                send_message("An error occurred while generating the report.")

        elif chat["content"] == "Please fill the email deatils":
            ask_email_info()

if "input_field" not in st.session_state:
    st.session_state.input_field = ""


user_prompt = st.text_input("You: ", key="input_field", on_change=on_submit)
