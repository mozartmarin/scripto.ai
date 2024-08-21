from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from google.oauth2 import service_account
from googleapiclient.discovery import build
from pydub import AudioSegment
from pydub.utils import mediainfo  # Adicionado para calcular a duração do vídeo
import io
import os
import speech_recognition as sr
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Obtém a chave da API do OpenAI a partir do arquivo .env
openai_api_key = os.getenv("OPENAI_API_KEY")

# Configura as embeddings do OpenAI usando a chave API
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

def authenticate_gdrive():
    """Autentica e retorna um serviço de API do Google Drive."""
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'C:/LangChain-Projects/tsvideos-6cfc82e1937a.json'

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('drive', 'v3', credentials=creds)
    return service

def download_video_from_gdrive(service, file_id):
    """Faz download de um vídeo do Google Drive e retorna o vídeo, o nome do arquivo e a duração."""
    request = service.files().get(fileId=file_id, fields="name")
    file_metadata = request.execute()
    file_name = file_metadata.get('name')

    request = service.files().get_media(fileId=file_id)
    video = io.BytesIO(request.execute())

    # Salva o vídeo temporariamente para calcular a duração
    with open("temp_video.mp4", "wb") as f:
        f.write(video.getbuffer())

    # Usa mediainfo para obter a duração do vídeo
    video_info = mediainfo("temp_video.mp4")
    duration = float(video_info['duration'])  # Duração em segundos

    return video, file_name, duration

def transcribe_video(video):
    """Transcreve o áudio do vídeo usando reconhecimento de fala."""
    # Converte o vídeo para áudio
    audio = AudioSegment.from_file(video, format="mp4")
    audio.export("temp.wav", format="wav")

    # Utiliza a biblioteca de reconhecimento de fala para transcrever o áudio
    recognizer = sr.Recognizer()
    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)
        try:
            transcription = recognizer.recognize_google(audio_data, language="pt-BR")
        except sr.UnknownValueError:
            transcription = "Could not understand audio"
        except sr.RequestError as e:
            transcription = f"Could not request results; {e}"

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
