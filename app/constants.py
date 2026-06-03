"""
Constants and configuration values for the Census RAG application.
"""

# Model Configuration
DEFAULT_MODEL_NAME = "Llama3-8b-8192"
DEFAULT_EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIMENSIONS = 768

# Text Splitting Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
MAX_DOCUMENTS_TO_PROCESS = 200

# Directory Paths
PDF_DATA_DIR = "End-to-End-RAG-Project-using-ObjectBox-and-Langchain/us-census-data"
OBJECTBOX_DB_DIR = "End-to-End-RAG-Project-using-ObjectBox-and-Langchain/objectbox"

# UI Configuration
APP_TITLE = "Census RAG: ObjectBox VectorstoreDB with LLAMA3"
APP_SUBTITLE = "Ask questions about US Census data using AI-powered retrieval"
PAGE_ICON = "📊"

# Prompt Template
RAG_PROMPT_TEMPLATE = """
Answer the questions based on the provided context only.
Please provide the most accurate response based on the question
<context>
{context}
<context>
Questions: {input}
"""

# Device Configuration
DEVICE = "cpu"  # Change to "cuda" if GPU is available
NORMALIZE_EMBEDDINGS = True
