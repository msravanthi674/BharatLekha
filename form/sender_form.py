import streamlit as st
import mysql.connector
from mysql.connector import Error

# MySQL connection setup
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="admin1234",  # Update this with your MySQL root password
            database="post_office"
        )
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
    return connection

# Function to generate a new unique ID
def generate_unique_id(table, prefix, cursor):
    query = f"SELECT MAX(CAST(SUBSTRING({table}_id, 2) AS UNSIGNED)) FROM {table}s"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    if result is None:
        new_id = f"{prefix}01"
    else:
        new_id = f"{prefix}{str(result + 1).zfill(2)}"
    return new_id

# Function to insert sender data
def insert_sender(connection, name, address, pincode, phone_number):
    cursor = connection.cursor()
    sender_id = generate_unique_id('sender', 's', cursor)
    query = """
    INSERT INTO senders (sender_id, sender_name, sender_address, sender_pincode, sender_phone_number)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (sender_id, name, address, pincode, phone_number))
    connection.commit()
    return sender_id

# Function to insert recipient data
def insert_recipient(connection, name, address, pincode, phone_number):
    cursor = connection.cursor()
    recipient_id = generate_unique_id('recipient', 'r', cursor)
    query = """
    INSERT INTO recipients (recipient_id, recipient_name, recipient_address, recipient_pincode, recipient_phone_number)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (recipient_id, name, address, pincode, phone_number))
    connection.commit()
    return recipient_id

# Function to insert delivery data
def insert_delivery(connection, sender_id, recipient_id, time_slot):
    cursor = connection.cursor()
    query = """
    INSERT INTO deliveries (sender_id, recipient_id, delivery_time_slot)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (sender_id, recipient_id, time_slot))
    connection.commit()

# Streamlit UI
st.title("Parcel Delivery System")

st.header("Sender Information")
sender_name = st.text_input("Sender Name")
sender_address = st.text_area("Sender Address")
sender_pincode = st.text_input("Sender Pincode")
sender_phone_number = st.text_input("Sender Phone Number")

st.header("Recipient Information")
recipient_name = st.text_input("Recipient Name")
recipient_address = st.text_area("Recipient Address")
recipient_pincode = st.text_input("Recipient Pincode")
recipient_phone_number = st.text_input("Recipient Phone Number")

st.header("Delivery Details")
delivery_time_slot = st.text_input("Preferred Delivery Time Slot")

if st.button("Submit"):
    if sender_name and sender_address and sender_pincode and sender_phone_number and recipient_name and recipient_address and recipient_pincode and recipient_phone_number and delivery_time_slot:
        connection = create_connection()
        if connection:
            sender_id = insert_sender(connection, sender_name, sender_address, sender_pincode, sender_phone_number)
            recipient_id = insert_recipient(connection, recipient_name, recipient_address, recipient_pincode, recipient_phone_number)
            insert_delivery(connection, sender_id, recipient_id, delivery_time_slot)
            st.success(f"Data stored successfully! Sender ID: {sender_id}, Recipient ID: {recipient_id}")
        else:
            st.error("Failed to connect to the database.")
    else:
        st.error("Please fill in all the details.")

