from langchain_community.vectorstores import Chroma
from langchain_dashscope import DashScopeEmbeddings, Tongyi
from langchain.chains import ConversationalRetrievalChain

def get_rag_chain(api_key):
    embeddings = DashScopeEmbeddings(dashscope_api_key=api_key)
    vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    llm = Tongyi(dashscope_api_key=api_key, model="qwen-turbo")
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
    return chain