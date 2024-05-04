import os
import streamlit as st
from streamlit_chat import message
import base64

from utills import load_embeddings
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA

from ingest import vector_embedding
from dotenv import load_dotenv
load_dotenv()

#api key
key=os.getenv("OPENAI_API_KEY")

st.title("Chat with PDF using GENIAI")
st.sidebar.title("File Details")


# Handling the pdf files
def display_pdf(file):
    with open(file,"rb") as file_obj:
        base64_pdf=base64.b64encode(file_obj.read()).decode("utf-8")
    pdf_display = f'<iframe  src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500"  type="application/pdf"></iframe>'
    st.markdown(pdf_display,unsafe_allow_html=True)

#llm pipeline
def llmpipeline():
    llm=ChatOpenAI(api_key=key,temperature=0.5)
    return llm


#builded qa llm
def qa_llm():
    llm=llmpipeline()
    persist_dirctory="temp/db"
    embedding=load_embeddings()
    vector_db=Chroma(persist_directory=persist_dirctory,embedding_function=embedding)
    retriever=vector_db.as_retriever()
    qa=RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=retriever,
    )
    return qa

def process_question(prompt):
    response=''
    prompt=prompt
    qa=qa_llm()
    generated_text=qa(prompt)
    response=generated_text['result']
    return response

def display_conversation(history):
    for i in range(len(history["generated"])):
        message(history["past"][i], is_user=True, key=str(i) + "_user")
        message(history["generated"][i],key=str(i))


def main():
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

        #Col divide
        col1,col2=st.columns([1,2])


        with col1:
            st.markdown("<h3 style=text-align:center> PDF Preview</h3>",unsafe_allow_html=True)
                    #Display files
            display_pdf(file_path)

        with col2:
            st.markdown("<h2 style=text-aligh:center> QA-Bot</h2>",unsafe_allow_html=True)
            with st.spinner("Embedding are in process.."):
                vector_embedding()
            st.success("Embeddings successfully done")
            st.markdown("<h4 style color:black;'>Chat Here</h4>", unsafe_allow_html=True)
            
            
            user_input=st.text_input("Prompt",key="input")

            if "generated" not in st.session_state:
                st.session_state["generated"]=["I am ready to help you"]
            if "past" not in st.session_state:
                st.session_state["past"]=["hey there"]

            if user_input:
                answer=process_question({'query':user_input})
                st.session_state["past"].append(user_input)

                response=answer
                st.session_state["generated"].append(response)

                   # Display conversation history using Streamlit messages
            if st.session_state["generated"]:
                display_conversation(st.session_state)


if __name__=="__main__":
    main()
                
