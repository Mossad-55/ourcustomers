import time

import streamlit as st
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd

connection_string = "mongodb+srv://mosad5:ScOrp555@matag-customers.d4c2idw.mongodb.net/?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
client = MongoClient(connection_string)


def create_document(collection, name, phone, address, rate):
    # Check if the document with the same name or phone number already exists
    existing_document = collection.find_one({"$or": [{"name": name}, {"phone": phone}]})

    if existing_document:
        st.warning("Document with the same name or phone number already exists!")
    else:
        document = {
            "name": name,
            "phone": phone,
            "address": address,
            "rate": rate
        }
        collection.insert_one(document)
        st.success("Customer created successfully!")


def delete_document(collection, name):
    collection.delete_one({"name": name})


def main():
    st.set_page_config(
        page_title="MATAG Company",
        page_icon="👋",
    )

    st.title("MATAG Company")

    db = client.customers
    collection = db.People

    page = st.sidebar.selectbox("Select Operation", ["All Customers", "Add Customer", "Delete Customer"])

    if page == "All Customers":
        st.header("Our Customers:")
        result = collection.find({})
        data = [doc for doc in result]
        df = pd.DataFrame(data)
        st.table(df)

    elif page == "Add Customer":
        st.header("Please enter the following data:")
        name = st.text_input("Name:")
        phone = st.text_input("Phone:")
        address = st.text_input("Address:")
        rate = st.slider("Rate", 0.0, 5.0, 0.0)

        if st.button("Create"):
            create_document(collection, name, phone, address, rate)

    elif page == "Delete Customer":
        st.header("Delete a Customer:")
        all_names = [doc["name"] for doc in collection.find({}, {"name": 1})]
        selected_name = st.selectbox("Select a Name to Delete", all_names)

        if st.button("Delete"):
            delete_document(collection, selected_name)
            st.success(f"Record for {selected_name} deleted successfully!")
            st.rerun()


if __name__ == '__main__':
    main()
