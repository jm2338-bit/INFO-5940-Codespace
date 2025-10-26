import streamlit as st
import os
from openai import OpenAI
from os import environ
import tempfile 

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

client = OpenAI(
	api_key=os.environ["API_KEY"],
	base_url="https://api.ai.it.cornell.edu",
)

st.title("📝 File Q&A with OpenAI")

# Allow multiple files  
uploaded_files = st.file_uploader("Upload a .txt or .pdf files", type=("txt","pdf"), accept_multiple_files=True)

# RAG 3.1 Document Ingestion and Chunking
@st.cache_resource(show_spinner="Processing document(s)...")
def get_retriever(cache_key, _uploaded_files):
    """
    Loads, splits, embeds, and indexes the uploaded documents.
    Returns a Chroma retriever object.
    """
    all_docs = []
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for uploaded_file in _uploaded_files:
            # Save file temporarily to disk 
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            # Load the document depending on file type
            if temp_path.endswith(".pdf"):
                loader = PyPDFLoader(temp_path)
            elif temp_path.endswith(".txt"):
                loader = TextLoader(temp_path)
            else:
                st.warning(f"Skipping unsupported file: {uploaded_file.name}")
                continue
            all_docs.extend(loader.load())

    if not all_docs:
        return None

    # Chunking Strategy
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(all_docs)

    # Initialize embedding model
    embeddings = OpenAIEmbeddings(model="openai.text-embedding-3-large",
                                  api_key=os.environ["API_KEY"])

    # Create Chroma vector store from chunks
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    # Create and return the retriever
    return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# Initialize retriever outside the chat logic
retriever = None
if uploaded_files:
    file_key = " ".join([f"{f.name}-{f.size}" for f in uploaded_files])
    retriever = get_retriever(file_key, uploaded_files)
else:
    st.cache_resource.clear() # clear cache if no files uploaded


# ---------- Chat Flow ----------

question = st.chat_input(
    "Ask something about the document(s)",
    disabled=not retriever,
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Upload a .txt or .pdf file(s) and ask a question."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if question and retriever:
    # RAG 3.2

    # Append the user's question to the messages
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    with st.chat_message("assistant"):
        # RAG 3.2: RAG Pipeline
        # 1. Retrieve and get relevant documents from Chroma
        with st.spinner("Retrieving relevant context..."):
            retrieved_docs = retriever.invoke(question)
        
        # st.json([doc.metadata for doc in retrieved_docs]) # Check if it is differentiating between different docs

        # 2. Augment 
        context_string = "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])
        # 3. Create RAG prompt
        rag_system_prompt = f"""
        You are an assistant for question-answering tasks.
        Use ONLY the following pieces of retrieved context to answer the question.
        If you don't know the answer, just say that you don't know.
        Keep the answer concise (three sentences maximum).

        Context:
        {context_string}
        """
        # 4. Generate
        stream = client.chat.completions.create(
            model="openai.gpt-4o",  # Change this to a valid model name
            messages=[
                {"role": "system", "content": rag_system_prompt},
                *st.session_state.messages
            ],
            stream=True
        )
        response = st.write_stream(stream)

    # Append the assistant's response to the messages
    st.session_state.messages.append({"role": "assistant", "content": response})