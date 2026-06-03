# Frequently Asked Questions (FAQ)

## General Questions

### What is Census RAG?
Census RAG is a Retrieval-Augmented Generation application that allows you to ask questions about US Census data using AI. It combines ObjectBox vector database with Groq's LLAMA3 model to provide accurate, context-aware answers.

### How does RAG work?
RAG (Retrieval-Augmented Generation) works in three steps:
1. **Retrieval**: Your question is converted to a vector and similar document chunks are found
2. **Augmentation**: Retrieved documents are added as context to your question
3. **Generation**: The LLM generates an answer based on the context

### Is my data private?
Yes! The vector database (ObjectBox) runs locally on your machine. Only your questions and retrieved context are sent to Groq for answer generation. The original documents never leave your device.

---

## Installation & Setup

### I'm getting "GROQ_API_KEY not found" error
Make sure you:
1. Created a `.env` file in the project root
2. Added `GROQ_API_KEY=your_key_here` to the file
3. Obtained an API key from [Groq Console](https://console.groq.com/)

### How do I get a Groq API key?
1. Visit [https://console.groq.com/](https://console.groq.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Generate a new API key
5. Copy and paste it into your `.env` file

### Installation fails with "No module named 'objectbox'"
Try installing the packages one by one:
```bash
pip install langchain-objectbox
pip install -r requirements.txt
```

If issues persist, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Usage Questions

### Do I need to click "Embedd Documents" every time?
No! Once you've embedded the documents, they're stored in the ObjectBox database. You only need to re-embed if:
- You add new PDF documents
- You delete the `objectbox/` directory
- You want to reprocess with different settings

### How long does embedding take?
Embedding 200 pages typically takes 2-5 minutes depending on your CPU. The progress spinner shows the process is running.

### Can I add my own PDF documents?
Yes! Place your PDFs in the `us-census-data/` directory and click "Embedd Documents" again to reprocess.

### What kind of questions can I ask?
You can ask any questions related to the content in the PDF documents:
- "What is the population of the United States?"
- "What are the demographic trends?"
- "How has migration changed over time?"

The better your question, the better the answer!

### Why is the answer incorrect or incomplete?
This can happen if:
1. **Information isn't in the documents**: The AI only uses provided PDFs
2. **Question is too vague**: Try being more specific
3. **Context is fragmented**: Try rephrasing to match document structure
4. **Model limitations**: LLAMA3 is powerful but not perfect

---

## Technical Questions

### Can I use a different LLM model?
Yes! Edit `constants.py` and change `DEFAULT_MODEL_NAME` to another Groq-supported model:
- `llama3-70b-8192` (larger, more capable)
- `mixtral-8x7b-32768` (longer context window)
- `gemma-7b-it`

### Can I use GPU acceleration?
Yes! Edit `constants.py` and change:
```python
DEVICE = "cuda"  # Instead of "cpu"
```

Make sure you have PyTorch with CUDA support installed.

### How do I change chunk size?
Edit `constants.py`:
```python
CHUNK_SIZE = 1500  # Increase for more context
CHUNK_OVERLAP = 300  # Increase proportionally
```

Larger chunks = more context but slower retrieval.

### Can I use a different embedding model?
Yes! Edit `constants.py`:
```python
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-l6-v2"
EMBEDDING_DIMENSIONS = 384  # Must match model dimensions
```

---

## Troubleshooting

### App is very slow
**Possible causes:**
1. **CPU-only inference**: Embeddings run on CPU by default
2. **Large documents**: Processing many large PDFs takes time
3. **Internet speed**: Groq API calls require internet

**Solutions:**
- Enable GPU acceleration (if available)
- Reduce `MAX_DOCUMENTS_TO_PROCESS` in `constants.py`
- Check your internet connection

### "Connection Error" when asking questions
**Causes:**
- No internet connection
- Groq API is down
- API rate limit exceeded

**Solutions:**
- Check internet connection
- Wait a few minutes and retry
- Check [Groq Status](https://status.groq.com/)

### ObjectBox database is corrupted
Delete the database and re-embed:
```bash
# Windows
rmdir /s /q objectbox
# Linux/Mac
rm -rf objectbox
```

Then click "Embedd Documents" in the app.

### High memory usage
**Normal for RAG applications!** Embeddings are memory-intensive.

**To reduce:**
- Lower `MAX_DOCUMENTS_TO_PROCESS` in `constants.py`
- Use smaller embedding model
- Process documents in batches

### Streamlit shows "Please wait..."
If the spinner runs forever:
1. Check terminal for error messages
2. Verify `.env` file exists with valid API key
3. Check PDF directory exists and has files
4. Restart the app

---

## Performance Optimization

### How can I make embedding faster?
1. Use GPU acceleration (`DEVICE = "cuda"`)
2. Reduce `MAX_DOCUMENTS_TO_PROCESS`
3. Use smaller embedding model (but may reduce accuracy)
4. Use fewer, more targeted documents

### How can I get better answers?
1. **Better questions**: Be specific and clear
2. **Better documents**: Add more relevant PDFs
3. **Tune chunk size**: Experiment with `CHUNK_SIZE`
4. **Better model**: Try larger LLM like `llama3-70b-8192`
5. **Adjust retrieval**: Modify retriever to return more/fewer chunks

---

## Development Questions

### Can I use this in production?
The current version is a proof-of-concept. For production:
- Add authentication
- Implement rate limiting
- Add monitoring and logging
- Use production-grade database setup
- Add comprehensive error handling
- Implement caching for common queries

### How do I contribute?
See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines!

### Can I integrate this with my app?
Yes! The core RAG logic can be extracted and used as a library. See `API.md` for usage examples.

---

## Common Errors

### `ModuleNotFoundError: No module named 'streamlit'`
```bash
pip install streamlit
```

### `FileNotFoundError: [Errno 2] No such file or directory: '.env'`
Create a `.env` file in the project root:
```bash
echo "GROQ_API_KEY=your_key_here" > .env
```

### `ValueError: GROQ_API_KEY not found in environment variables`
Your `.env` file is missing or malformed. Ensure it contains:
```
GROQ_API_KEY=gsk_...
```

---

## Still Need Help?

- 📧 Email: nebeyoumusie@gmail.com
- 💼 LinkedIn: [Nebeyou Musie](https://www.linkedin.com/in/nebeyou-musie)
- 💬 Telegram: [@NebeyouMusie](https://t.me/NebeyouMusie)
- 🐛 GitHub Issues: [Create an issue](https://github.com/harshkushwaha7x/census-rag-objectbox/issues)
