from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from config import load_config, get_groq_api
from constants import DEFAULT_MODEL_NAME, DEFAULT_EMBEDDING_MODEL, DEVICE, NORMALIZE_EMBEDDINGS
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
        
        llm = ChatGroq(groq_api_key=api_key, model_name=DEFAULT_MODEL_NAME)
        logger.info(f"Groq LLM initialized successfully with model: {DEFAULT_MODEL_NAME}")
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
                    model_name=DEFAULT_EMBEDDING_MODEL,
                    model_kwargs={'device': DEVICE},
                    encode_kwargs={'normalize_embeddings': NORMALIZE_EMBEDDINGS}
        )
        logger.info(f"HuggingFace embeddings initialized successfully with model: {DEFAULT_EMBEDDING_MODEL}")
        return embeddings
    except Exception as e:
        logger.error(f"Error initializing embeddings: {str(e)}")
        raise