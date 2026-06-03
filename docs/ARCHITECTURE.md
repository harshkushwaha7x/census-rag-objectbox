# Census RAG Architecture

## Overview

Census RAG is a Retrieval-Augmented Generation (RAG) application that combines vector search with large language models to answer questions about US Census data.

## System Architecture

```
┌─────────────────┐
│   User Input    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Streamlit UI   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│         RAG Pipeline                │
│  ┌──────────────────────────────┐  │
│  │  1. Query Embedding          │  │
│  │     (HuggingFace BGE)        │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│             ▼                       │
│  ┌──────────────────────────────┐  │
│  │  2. Vector Search            │  │
│  │     (ObjectBox)              │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│             ▼                       │
│  ┌──────────────────────────────┐  │
│  │  3. Context Retrieval        │  │
│  │     (Top-K Documents)        │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│             ▼                       │
│  ┌──────────────────────────────┐  │
│  │  4. Answer Generation        │  │
│  │     (Groq LLAMA3)            │  │
│  └──────────┬───────────────────┘  │
└─────────────┼───────────────────────┘
              │
              ▼
┌─────────────────────────────┐
│    Response to User         │
└─────────────────────────────┘
```

## Components

### 1. Document Processing
- **PDF Loader**: `PyPDFDirectoryLoader` loads PDF files from the data directory
- **Text Splitter**: `RecursiveCharacterTextSplitter` chunks documents into 1000-character segments with 200-character overlap
- **Chunking Strategy**: Overlapping chunks ensure context preservation across boundaries

### 2. Embedding Layer
- **Model**: HuggingFace BGE (BAAI/bge-small-en-v1.5)
- **Dimensions**: 768-dimensional vectors
- **Device**: CPU-based inference (configurable for GPU)
- **Normalization**: L2 normalization for cosine similarity

### 3. Vector Database
- **Technology**: ObjectBox
- **Storage**: Local, on-device vector store
- **Benefits**: 
  - Fast retrieval
  - No network latency
  - Data privacy (no cloud dependency)
  - Persistent storage

### 4. Language Model
- **Provider**: Groq
- **Model**: LLAMA3-8B-8192
- **Context Window**: 8192 tokens
- **Inference**: Fast, cloud-based inference

### 5. RAG Chain
- **Document Chain**: Combines retrieved documents with the prompt
- **Retrieval Chain**: Orchestrates query → retrieval → generation pipeline
- **Prompt Template**: Custom template for context-aware responses

## Data Flow

1. **Initialization Phase**
   - Load PDF documents
   - Split into chunks
   - Generate embeddings
   - Store in ObjectBox

2. **Query Phase**
   - User submits question
   - Question is embedded
   - Vector similarity search finds relevant chunks
   - Chunks are sent to LLM with question
   - LLM generates contextual answer

3. **Response Phase**
   - Answer displayed to user
   - Source documents shown for transparency
   - Response time tracked

## Configuration

All configuration is centralized in `constants.py`:
- Model names
- Chunk sizes
- File paths
- Embedding dimensions

## Scalability Considerations

- **Document Volume**: Currently processes 200 documents; adjustable via `MAX_DOCUMENTS_TO_PROCESS`
- **Chunk Size**: Optimized for 1000 characters; tune based on document structure
- **Embedding Model**: Can swap for larger models if accuracy is priority
- **LLM**: Can switch to other Groq models or providers

## Security

- API keys stored in `.env` file (not committed)
- Local vector storage (no data sent to cloud for storage)
- Groq API calls encrypted (HTTPS)

## Performance

- **Embedding Generation**: ~1-2 seconds per document
- **Vector Search**: <100ms for typical queries
- **LLM Inference**: ~2-4 seconds via Groq
- **Total Query Time**: ~3-5 seconds

## Future Enhancements

- [ ] Multi-language support
- [ ] Hybrid search (keyword + semantic)
- [ ] Query result caching
- [ ] Conversation memory
- [ ] Fine-tuned embeddings for census domain
