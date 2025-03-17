import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from streamlit_option_menu import option_menu
import pandas  as pd
from PIL import Image
import base64
import os
import requests
container_pdf, container_chat = st.columns([50, 50])
# Initialize AWS Textract Client
# Title of the app


def analyze_invoice(payload):
    url = "https://1qukft6pvi.execute-api.us-east-1.amazonaws.com/v1/inovice-automated"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url,json=payload, headers=headers).json()
    keys,values = response.keys(), response.values()
    print(response)
    # for i in response["fields"]:
    #     keys.append(i["Alias"])
    #     values.append(i["Value"])

    df = pd.DataFrame({"Field":keys,  "Value":values})
    return df

# Streamlit UI

with st.sidebar:
    selected = option_menu("Main Menu", ["HOME","Invoice OCR"],
     icons=['house','bi-file-earmark-break'], menu_icon="cast", default_index=0)

if selected == "HOME":
    st.image("./img/Logo.svg")
    st.title("Invoice Data Extractor Demo")
    st.info('for Sarang')

    image = Image.open("./img/Homepage.png")
# Display image
    st.image(image, caption="Sample Invoice")

elif selected == "Invoice OCR":
    st.title("📄 Invoice Data Extractor")

    # File Upload
    uploaded_file = st.file_uploader("Upload an Invoice (JPG, PNG, or PDF)", type=["jpg", "jpeg", "png", "pdf"])
    if uploaded_file is not None:
        # Read File Bytes
        file_bytes = uploaded_file.read()

        # Process File
        with st.spinner("Extracting Invoice Data..."):
            df = analyze_invoice({"file_name":uploaded_file.name, "file_content": base64.b64encode(file_bytes).decode("utf-8")})
        if not df.empty:
            st.success("✅ Invoice Data Extracted Successfully!")
            st.dataframe(df)
        else:
            st.error("❌ No key-value pairs found in the document.")

       

    