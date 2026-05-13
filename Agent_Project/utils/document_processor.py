import os
import hashlib
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_dashscope import DashScopeEmbeddings

def get_file_md5(file_content):
    return hashlib.md5(file_content).hexdigest()

def process_uploaded_files(uploaded_files, api_key):
    if not os.path.exists("data"):
        os.makedirs("data")
    embeddings = DashScopeEmbeddings(dashscope_api_key=api_key)
    vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    total_chunks = 0
    for uploaded_file in uploaded_files:
        file_bytes = uploaded_file.read()
        file_md5 = get_file_md5(file_bytes)
        temp_file_path = os.path.join("data", uploaded_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(file_bytes)
        loader = TextLoader(temp_file_path, encoding='utf-8')
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(documents)
        for chunk in chunks:
            chunk.metadata["file_md5"] = file_md5
        vectorstore.add_documents(chunks)
        total_chunks += len(chunks)
    return total_chunks