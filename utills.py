import os
from dotenv import load_dotenv
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

# load_dotenv()

key=os.getenv("OPENAI_API_KEY")

#Load Doc
def load_file(directory):
    try:
        for files in os.listdir(directory):
            if files.endswith(".pdf"):
                loader=PyPDFLoader(os.path.join(directory,files))
                docs=loader.load()
                return docs
    except Exception as e:
        raise Exception("No pdf file found",e)
    

#Split documents
def doc_spliter(documents):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    docs=text_splitter.split_documents(documents)
    return docs

#Embeddings
def load_embeddings():
    embeddings=OpenAIEmbeddings(api_key=key)
    return embeddings


# def load(file_path):
#     for files in os.listdir(file_path):
#     # Check if the file is a PDF file
#         if files.endswith(".pdf"):
#             # Load the PDF file using PyPDFLoader
#             loader = PyPDFLoader(os.path.join(file_path,files))
#             docs = loader.load()
#             # Now you can do something with the loaded PDF file
#             print(docs)
# if __name__=="__main__":
#     load_file("docs")
#     # print(docs)




