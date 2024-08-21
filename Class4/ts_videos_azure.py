from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import requests
import os

# Carrega as variáveis de ambiente
load_dotenv()

# Obtém a chave da API do OpenAI a partir do arquivo .env
openai_api_key = os.getenv("OPENAI_API_KEY")

# Configura as embeddings do OpenAI usando a chave API
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

def transcribe_video_azure(video_url):
    """Transcreve o áudio de um vídeo usando o Azure Video Index."""
    token_url = f"https://login.microsoftonline.com/{os.getenv('AZURE_TENANT_ID')}/oauth2/v2.0/token"
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': os.getenv('AZURE_CLIENT_ID'),
        'client_secret': os.getenv('AZURE_CLIENT_SECRET'),
        'scope': 'https://management.azure.com/.default'
    }
    token_response = requests.post(token_url, data=token_data)
    token = token_response.json().get('access_token')

    # Fazer a transcrição usando Azure Video Index
    index_url = f"https://<your-regional-endpoint>/media/{os.getenv('AZURE_API_VERSION')}/videos"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    index_data = {
        "url": video_url
    }
    response = requests.post(index_url, headers=headers, json=index_data)
    if response.status_code == 200:
        transcription = response.json().get('transcription', 'Transcription not available')
    else:
        transcription = "Error in transcription"
    
    return transcription

def create_vector_from_transcript(transcription):
    """Cria uma base de vetores FAISS a partir da transcrição."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents([transcription])

    db = FAISS.from_documents(docs, embeddings)
    return db

def format_transcript(transcript):
    """Formata a transcrição com quebras de linha e estrutura."""
    if isinstance(transcript, str):
        return transcript  # Se já for uma string, retorne diretamente
    else:
        # Se for uma lista de objetos (caso não esperado), manter a lógica antiga
        formatted_text = "\n".join([t.page_content for t in transcript])
        return formatted_text
