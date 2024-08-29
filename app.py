import streamlit as st
import mysql.connector
from datetime import datetime, time
from twilio.rest import Client

# Replace with your actual database connection details
def get_db_connection():
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',  # Replace with your MySQL username
        password='admin123',  # Replace with your MySQL password
        database='sih'  # Use your database name
    )
    return connection

# Twilio credentials
TWILIO_ACCOUNT_SID = 'AC1dc1625309ca4237753fab4c2c38a7b4'
TWILIO_AUTH_TOKEN = '12b9ac11372728e504de0a3cda0f07e7'
TWILIO_PHONE_NUMBER = '+12568576868'

# Define time slots
time_slots = [
    (time(9, 0), time(10, 0)),
    (time(10, 0), time(11, 0)),
    (time(11, 0), time(12, 0)),
    (time(12, 0), time(13, 0)),
    (time(13, 0), time(14, 0)),
    (time(14, 0), time(15, 0)),
    (time(15, 0), time(16, 0)),
    (time(16, 0), time(17, 0))
]

def map_to_time_slot(selected_time):
    for slot_start, slot_end in time_slots:
        if slot_start <= selected_time < slot_end:
            return f"{slot_start.strftime('%H:%M')} - {slot_end.strftime('%H:%M')}"
    return None

def send_sms(recipient_phone_number, consignment_id, recipient_name, time_slot, recipient_address):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"The delivery time scheduled for '{consignment_id}' order for '{recipient_name}' is '{time_slot}' at '{recipient_address}'.",
        from_=TWILIO_PHONE_NUMBER,
        to=recipient_phone_number
    )
    return message.sid

# Streamlit form
st.title("Consignment Form")

with st.form("consignment_form"):
    consignment_id = st.text_input("Consignment ID")
    sender_name = st.text_input("Sender Name")
    recipient_name = st.text_input("Recipient Name")
    item_type = st.text_input("Item Type")
    recipient_phone_number = st.text_input("Recipient Phone Number")
    sender_phone_number = st.text_input("Sender Phone Number")
    initial_time_schedule = st.time_input("Initial Time Schedule", time(13, 15))
    recipient_address = st.text_area("Recipient Address")
    sender_pincode = st.text_input("Sender Pincode")
    pincode = st.text_input("Pincode")
    
    submit_button = st.form_submit_button(label="Submit")
    send_sms_button = st.form_submit_button(label="Send SMS")

if submit_button:
    time_slot = map_to_time_slot(initial_time_schedule)
    if time_slot:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
            INSERT INTO form (consignment_id, sender_name, recipient_name, item_type, recipient_phone_number, sender_phone_number, initial_time_schedule, recipient_address, sender_pincode, pincode, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """
            cursor.execute(query, (consignment_id, sender_name, recipient_name, item_type, recipient_phone_number, sender_phone_number, datetime.combine(datetime.now().date(), initial_time_schedule), recipient_address, sender_pincode, pincode))
            conn.commit()
            cursor.close()
            conn.close()
            st.success("Data has been successfully inserted into the database!")
        except Exception as e:
            st.error(f"Error inserting data into the database: {str(e)}")
    else:
        st.error("The selected time does not match any predefined time slots.")

if send_sms_button:
    time_slot = map_to_time_slot(initial_time_schedule)
    if time_slot:
        try:
            sms_sid = send_sms(recipient_phone_number, consignment_id, recipient_name, time_slot, recipient_address)
            st.info(f"SMS sent successfully! Message SID: {sms_sid}")
        except Exception as e:
            st.error(f"Error sending SMS: {str(e)}")
    else:
        st.error("The selected time does not match any predefined time slots.")
