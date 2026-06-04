# Census RAG: ObjectBox & LangChain

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.20-green.svg)](https://www.langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

> An advanced RAG (Retrieval-Augmented Generation) system that uses ObjectBox vector database and Groq's LLAMA3 model to intelligently retrieve and answer questions from US Census PDF documents.

![Streamlit Web App Interface](./images/RAG%20app%20UI.png)

## 🌟 Features

- 📊 **Local Vector Database**: Uses ObjectBox for efficient, on-device vector storage
- 🤖 **Powered by LLAMA3**: Leverages Groq's LLAMA3-8B model for intelligent responses
- 📄 **Multi-PDF Support**: Process and query multiple US Census PDF documents
- ⚡ **Fast Retrieval**: Quick semantic search and answer generation
- 🎨 **Clean UI**: User-friendly Streamlit interface with real-time feedback
- 🔒 **Privacy-Focused**: All data processing happens locally

## 🎬 DEMO
 - You can check the project live [here](https://8512-01hwj8ynshjz7spkr595x77ec2.cloudspaces.litng.ai/)

## 📖 Description

This project showcases the implementation of an advanced RAG system that uses ObjectBox vector database and Groq's LLAMA3 model as an LLM to retrieve information from US Census PDF documents.

### 🔧 Technical Implementation

1. **Document Loading**: Used `PyPDFDirectoryLoader` from `langchain_community` to load PDF documents from the `us-census-data` directory
2. **Text Chunking**: Transformed each text into chunks of 1000 characters using `RecursiveCharacterTextSplitter` with 200 character overlap
3. **Embeddings**: Created vector embeddings using `HuggingFaceBgeEmbeddings` (BAAI/bge-small-en-v1.5 model)
4. **Vector Storage**: Stored embeddings in `ObjectBox` vector store for efficient retrieval
5. **LLM Setup**: Configured `ChatGroq` with Llama3-8b-8192 model
6. **Prompt Engineering**: Designed custom `ChatPromptTemplate` for context-aware responses
7. **RAG Pipeline**: Created `document_chain` and `retrieval_chain` for seamless question answering

## 🛠️ Technologies Used

- **LangChain** (0.1.20) - Framework for LLM applications
- **ObjectBox** - High-performance vector database
- **Groq** - Fast LLM inference with LLAMA3
- **HuggingFace** - BGE embeddings model
- **Streamlit** - Interactive web interface
- **PyPDF** - PDF document processing

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Git
- Groq API key ([Get one here](https://console.groq.com/))

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/harshkushwaha7x/census-rag-objectbox.git
   cd census-rag-objectbox
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   ```bash
   # Copy the example environment file
   copy .env.example .env  # Windows
   cp .env.example .env    # macOS/Linux
   
   # Edit .env and add your Groq API key
   GROQ_API_KEY=your_actual_api_key_here
   ```

5. **Run the Application**
   ```bash
   cd app
   streamlit run app.py
   ```

6. **Access the Application**
   - Open your browser and navigate to `http://localhost:8501`
   - Click "Embedd Documents" button (if needed)
   - Start asking questions about US Census data!

## 🚀 Usage

1. **First Time Setup**: Click the "📚 Embedd Documents" button to process and store PDF documents
2. **Ask Questions**: Enter questions in the text input field
3. **View Results**: Get AI-generated answers with source document references
4. **Explore Context**: Expand "Document Similarity Search Results" to see retrieved chunks

## 🐳 Docker Deployment

### Quick Start with Docker Compose

1. **Setup Environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

2. **Build and Run**
   ```bash
   docker-compose up -d
   ```

3. **Access Application**
   - Open browser to `http://localhost:8501`

4. **View Logs**
   ```bash
   docker-compose logs -f
   ```

5. **Stop Application**
   ```bash
   docker-compose down
   ```

### Using Docker Only

```bash
# Build image
docker build -t census-rag:latest .

# Run container
docker run -d \
  --name census-rag \
  -p 8501:8501 \
  -v $(pwd)/objectbox:/app/objectbox \
  -e GROQ_API_KEY=your_api_key_here \
  census-rag:latest
```

For detailed deployment options (AWS, GCP, Azure, Heroku), see [DEPLOYMENT.md](./docs/DEPLOYMENT.md)

## 📚 Documentation

- [Architecture Overview](./docs/ARCHITECTURE.md) - System design and data flow
- [API Documentation](./docs/API.md) - Module and function reference
- [FAQ & Troubleshooting](./docs/FAQ.md) - Common questions and solutions
- [Deployment Guide](./docs/DEPLOYMENT.md) - Production deployment options





## 🤝 Contributing

Contributions are welcome! Please check out our [Contributing Guidelines](./CONTRIBUTING.md) for details on how to get started.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## 🙏 Acknowledgments

- [Krish Naik](https://www.youtube.com/@krishnaik06) for educational content and inspiration
- [ObjectBox](https://objectbox.io/) for the vector database
- [Groq](https://groq.com/) for fast LLM inference
- [LangChain](https://www.langchain.com/) for the RAG framework

## 📧 Contact

**Nebeyou Musie**
- 💼 LinkedIn: [Nebeyou Musie](https://www.linkedin.com/in/nebeyou-musie)
- 📧 Email: nebeyoumusie@gmail.com
- 💬 Telegram: [@NebeyouMusie](https://t.me/NebeyouMusie)

---

⭐ Star this repository if you find it helpful!
