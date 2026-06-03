# API Documentation

## Module Overview

Census RAG consists of several key modules that work together to provide RAG functionality.

---

## `config.py`

Configuration management for the application.

### Functions

#### `load_config()`
Load environment variables from .env file.

**Returns:**
- `bool`: True if .env file was loaded successfully, False otherwise

**Example:**
```python
from config import load_config
load_config()
```

---

#### `get_groq_api()`
Retrieve Groq API key from environment variables.

**Returns:**
- `str`: Groq API key or None if not found

**Example:**
```python
from config import get_groq_api
api_key = get_groq_api()
```

---

#### `get_config_value(key, default=None)`
Get configuration value from environment variables.

**Parameters:**
- `key` (str): Environment variable name
- `default`: Default value if key not found

**Returns:**
- Configuration value or default

**Example:**
```python
from config import get_config_value
model_name = get_config_value("MODEL_NAME", "Llama3-8b-8192")
```

---

## `utils.py`

Utility functions for LLM and embeddings initialization.

### Functions

#### `groq_llm()`
Initialize and return ChatGroq LLM instance.

**Returns:**
- `ChatGroq`: Configured Groq LLM instance

**Raises:**
- `ValueError`: If GROQ_API_KEY is not set

**Example:**
```python
from utils import groq_llm

llm = groq_llm()
response = llm.invoke("What is RAG?")
```

---

#### `huggingface_instruct_embedding()`
Initialize and return HuggingFace BGE embeddings instance.

**Returns:**
- `HuggingFaceBgeEmbeddings`: Configured embeddings instance

**Example:**
```python
from utils import huggingface_instruct_embedding

embeddings = huggingface_instruct_embedding()
vector = embeddings.embed_query("Sample text")
```

---

## `constants.py`

Application constants and configuration values.

### Constants

#### Model Configuration
- `DEFAULT_MODEL_NAME`: "Llama3-8b-8192"
- `DEFAULT_EMBEDDING_MODEL`: "BAAI/bge-small-en-v1.5"
- `EMBEDDING_DIMENSIONS`: 768

#### Text Processing
- `CHUNK_SIZE`: 1000
- `CHUNK_OVERLAP`: 200
- `MAX_DOCUMENTS_TO_PROCESS`: 200

#### Directory Paths
- `PDF_DATA_DIR`: Path to PDF documents
- `OBJECTBOX_DB_DIR`: Path to ObjectBox database

#### UI Configuration
- `APP_TITLE`: Application title
- `APP_SUBTITLE`: Application subtitle
- `PAGE_ICON`: Page icon emoji

---

## `app.py`

Main Streamlit application.

### Functions

#### `vector_embedding()`
Load PDF documents, split into chunks, and create ObjectBox vector store.

**Returns:**
- `bool`: True if successful, False otherwise

**Side Effects:**
- Initializes `st.session_state.embeddings`
- Initializes `st.session_state.loader`
- Initializes `st.session_state.docs`
- Initializes `st.session_state.text_splitter`
- Initializes `st.session_state.final_documents`
- Initializes `st.session_state.vectors`

**Example:**
```python
if vector_embedding():
    print("Documents embedded successfully")
```

---

## Usage Examples

### Basic RAG Query Flow

```python
from utils import groq_llm, huggingface_instruct_embedding
from langchain_objectbox.vectorstores import ObjectBox
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Initialize components
llm = groq_llm()
embeddings = huggingface_instruct_embedding()

# Load vector store (assuming already populated)
vectorstore = ObjectBox(
    embedding=embeddings,
    embedding_dimensions=768,
    db_directory="./objectbox"
)

# Create retrieval chain
prompt = ChatPromptTemplate.from_template(
    "Answer based on context: {context}\nQuestion: {input}"
)
document_chain = create_stuff_documents_chain(llm, prompt)
retriever = vectorstore.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

# Query
response = retrieval_chain.invoke({"input": "What is the population?"})
print(response["answer"])
```

---

## Environment Variables

Required environment variables:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GROQ_API_KEY` | Groq API key for LLM access | Yes | None |
| `MODEL_NAME` | LLM model name | No | Llama3-8b-8192 |
| `EMBEDDING_MODEL` | Embedding model name | No | BAAI/bge-small-en-v1.5 |

---

## Error Handling

All functions include try-catch error handling with logging:

```python
try:
    # Operation
except Exception as e:
    logger.error(f"Error: {str(e)}")
    raise
```

Errors are logged and re-raised for proper handling at higher levels.

---

## Testing

To test individual components:

```python
# Test config loading
from config import load_config, get_groq_api
load_config()
assert get_groq_api() is not None

# Test LLM initialization
from utils import groq_llm
llm = groq_llm()
assert llm is not None

# Test embeddings
from utils import huggingface_instruct_embedding
embeddings = huggingface_instruct_embedding()
vector = embeddings.embed_query("test")
assert len(vector) == 768
```
