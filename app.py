import os
import streamlit as st
import base64
st.title("Chat with PDF using GENIAI")
st.sidebar.title("File Details")
# Handling the pdf files
def display_pdf(file):
    with open(file,"rb") as file_obj:
        base64_pdf=base64.b64encode(file_obj.read()).decode("utf-8")
    pdf_display = f'<iframe  src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500"  type="application/pdf"></iframe>'
    st.markdown(pdf_display,unsafe_allow_html=True)


file_upload=st.sidebar.file_uploader("Upload file...",type=["pdf","docx"])
if file_upload:
    st.sidebar.success("File Uploaded successfully",icon="✅")
    file_name=file_upload.name # file name
    file_size=len(file_upload.read()) # get file size in bytes
    st.sidebar.markdown("<h3 style=text-align:center>File Details</h3>",unsafe_allow_html=True)
    file_details={
        "file_name":file_name,
        "file_size":file_size
    }
    st.sidebar.json(file_details) 
    #save locally
    file_dir="docs"
    os.makedirs(file_dir,exist_ok=True)
    file_path="docs/"+file_upload.name
    with open(file_path,"wb") as f:
        f.write(file_upload.getbuffer())
    col1,col2=st.columns([1,2])
    with col1:
        st.markdown("<h3 style=text-align:center> PDF Preview</h3>",unsafe_allow_html=True)
                #Display files
        display_pdf(file_path)
    with col2:
        st.markdown("<h2 style=text-aligh:center> QA-Bot</h2>",unsafe_allow_html=True)

        if "generated" not in st.session_state:
            st.session_state["generated"]=["I am ready to help you"]
        if "past" not in st.session_state:
            st.session_state["past"]=["hey there"]
            
# else:
#     st.sidebar.error("Please upload a pdf/doc file",icon="🚨")