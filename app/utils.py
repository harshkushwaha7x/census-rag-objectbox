from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from config import load_config, get_groq_api
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# load app configuration
load_config()


# setup groq LLM
def groq_llm():
    """
    Initialize and return ChatGroq LLM instance.
    
    Returns:
        ChatGroq: Configured Groq LLM instance
        
    Raises:
        ValueError: If GROQ_API_KEY is not set
    """
    try:
        api_key = get_groq_api()
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        llm = ChatGroq(groq_api_key=api_key, model_name='Llama3-8b-8192')
        logger.info("Groq LLM initialized successfully")
        return llm
    except Exception as e:
        logger.error(f"Error initializing Groq LLM: {str(e)}")
        raise

# setup huggingface_instruct_embedding
def huggingface_instruct_embedding():
    """
    Initialize and return HuggingFace BGE embeddings instance.
    
    Returns:
        HuggingFaceBgeEmbeddings: Configured embeddings instance
    """
    try:
        embeddings = HuggingFaceBgeEmbeddings(
                    model_name='BAAI/bge-small-en-v1.5',  #sentence-transformers/all-MiniLM-l6-v2
                    model_kwargs={'device': 'cpu'},
                    encode_kwargs={'normalize_embeddings': True}
        )
        logger.info("HuggingFace embeddings initialized successfully")
        return embeddings
    except Exception as e:
        logger.error(f"Error initializing embeddings: {str(e)}")
        raise