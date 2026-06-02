# import all necessary libraries
import time
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_objectbox.vectorstores import ObjectBox
from langchain_core.prompts import ChatPromptTemplate
from utils import groq_llm, huggingface_instruct_embedding

# Page configuration
st.set_page_config(
    layout='wide', 
    page_title="Census RAG - ObjectBox & LangChain",
    page_icon="📊"
)

st.title('📊 Census RAG: ObjectBox VectorstoreDB with LLAMA3')
st.markdown("### Ask questions about US Census data using AI-powered retrieval")

prompt = ChatPromptTemplate.from_template(
    """
    
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question
    <context>
    {context}
    <context>
    Questions: {input}

    """
)

# function for vector embedding and Objectbox VectorstoreDB
def vector_embedding():
    """
    Load PDF documents, split into chunks, and create ObjectBox vector store.
    """
    if 'vectors' not in st.session_state:
        with st.spinner('Processing documents... This may take a few minutes.'):
            try:
                st.session_state.embeddings = huggingface_instruct_embedding()
                st.session_state.loader = PyPDFDirectoryLoader('End-to-End-RAG-Project-using-ObjectBox-and-Langchain/us-census-data')
                st.session_state.docs = st.session_state.loader.load()
                st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:200])
                st.session_state.vectors = ObjectBox.from_documents(
                    st.session_state.final_documents, 
                    st.session_state.embeddings, 
                    embedding_dimensions=768, 
                    db_directory='End-to-End-RAG-Project-using-ObjectBox-and-Langchain/objectbox'
                )
                st.success('✅ Documents processed and embedded successfully!')
            except Exception as e:
                st.error(f'❌ Error processing documents: {str(e)}')
                return False
    return True


if st.button('📚 Embedd Documents'):
    vector_embedding()

st.markdown("---")
user_input = st.text_input('💬 Enter your question from documents', placeholder="e.g., What is the population trend in the US?")


if user_input:
    if 'vectors' not in st.session_state:
        st.warning('⚠️ Please embed documents first by clicking the "Embedd Documents" button above.')
    else:
        try:
            with st.spinner('🔍 Searching for answer...'):
                document_chain = create_stuff_documents_chain(groq_llm(), prompt)
                retriever = st.session_state.vectors.as_retriever()
                retrieval_chain = create_retrieval_chain(retriever, document_chain)
                start = time.process_time()

                response = retrieval_chain.invoke({'input': user_input})
                
                st.markdown("### 📝 Answer:")
                st.write(response['answer'])
                st.info(f'⏱️ Response time: {(time.process_time() - start):.2f} seconds')

            # With a streamlit expander
            with st.expander("📄 Document Similarity Search Results"):
                # Find the relevant chunks
                for i, doc in enumerate(response["context"]):
                    st.markdown(f"**Document {i+1}:**")
                    st.write(doc.page_content)
                    st.markdown("---")
        except Exception as e:
            st.error(f'❌ Error generating response: {str(e)}')

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This application uses:
    - **ObjectBox** for vector storage
    - **LLAMA3** (via Groq) for question answering
    - **LangChain** for RAG pipeline
    - **HuggingFace BGE** embeddings
    
    **Data Source:** US Census Bureau documents
    """)
    
    if 'vectors' in st.session_state:
        st.success("✅ Database Ready")
    else:
        st.warning("⚠️ Database Not Initialized")