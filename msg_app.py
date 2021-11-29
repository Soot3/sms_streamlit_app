from datetime import datetime
import streamlit as st
from octopush import SMS
import requests
import json

# Authentication from environment variables
login = st.secrets["api_login"]
auth_key = st.secrets["api_key"]


st.title("SMS Scheduler (Octopush Web App)")
st.header("This app uses the Octopush API to schedule messages to mobile phones")

st.write("Octopush allows you to automate sending SMS with your applications, software and information systems.")
st.write ("With Octopush you can send SMS messages to more than 196 countries using their SMS API")
st.markdown("Code for this app can be found [here](https://github.com/Soot3/sms_streamlit_app)")

info_form = st.form(key = "info",clear_on_submit=True)

msg_val = info_form.text_input(label='What message do you want to send')
recipent_val = info_form.text_input(label="Input recipent")
recipent_val1 = info_form.text_input(label="Input recipient first name")
recipent_val2 = info_form.text_input(label="Input recipient last name")
sender_val = info_form.text_input(label="Input Sender name ")
date_val = info_form.date_input("Scheduled date")
time_val = info_form.time_input("Scheduled time")
type_val = info_form.text_input(label='What type of message are you sending', value = '[sms_premium or sms_low_cost]')
purpose_val = info_form.text_input(label='What purpose is the message sent for', value = '[alert or wholesale]')
replies_val = info_form.text_input(label='Accept replies?', value = '[True or False]')

submit_button = info_form.form_submit_button(label='Submit')

if submit_button:        
    dateandtime = f"{date_val} {time_val}"
    send_date = datetime.strptime(dateandtime, '%Y-%m-%d %H:%M:%S')
    send_date = str(send_date.isoformat())
    recipients_val_split = [{"phone_number": recipent_val,"first_name":recipent_val1, "last_name":recipent_val2}]
    credit_result = requests.get("https://api.octopush.com/v1/public/wallet/check-balance", headers={"api-login":login,"api-key":auth_key}, params={"with_details":True})
    
    parameters = {"text":msg_val, "recipients":recipients_val_split, "type":type_val,"sender":sender_val, "send_at":send_date,"purpose":purpose_val,"with_replies":replies_val}

    result = requests.post("https://api.octopush.com/v1/public/sms-campaign/send", headers={"api-login":login,"api-key":auth_key}, data=json.dumps(parameters))

    st.write("Credit Check")
    st.write(credit_result.text)

    st.write("Message result")
    st.write(result)
    st.write(result.text)
