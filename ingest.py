import os
from utills import load_file,doc_spliter,load_embeddings

from langchain_community.vectorstores import Chroma

persist_directory="temp/db"

file_dir="docs"

def vector_embedding():
    #Load file
    loader=load_file(file_dir)
    #chunks
    text_chunks=doc_spliter(loader)
    #Embeddings 
    embeddings=load_embeddings()

    #Store Vector
    vector_db=Chroma.from_documents(text_chunks,embeddings,persist_directory=persist_directory)
    vector_db.persist()