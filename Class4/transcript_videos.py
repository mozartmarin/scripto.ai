# %%
from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

# %%
# Carrega as variáveis de ambiente
load_dotenv()

# %%
# Obtém a chave da API do OpenAI a partir do arquivo .env
openai_api_key = os.getenv("OPENAI_API_KEY")

# %%
# Configura as embeddings do OpenAI usando a chave API
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# %%
# Função para carregar a transcrição do vídeo do YouTube
def load_transcript(video_url: str):
    loader = YoutubeLoader.from_youtube_url(video_url, language="pt")
    transcript = loader.load()
    return transcript

# %%
# Função para criar vetor a partir da transcrição do vídeo do YouTube
def create_vector_from_transcript(transcript) -> FAISS:
    # Divide a transcrição em partes menores
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(transcript)

    # Cria uma base de vetores FAISS a partir dos documentos
    db = FAISS.from_documents(docs, embeddings)
    return db

# %%
# Função para obter resposta baseada em consulta na base de vetores
def get_response_from_query(db, query, k=4):
    # Realiza uma busca por similaridade nos vetores
    docs = db.similarity_search(query, k=k)
    docs_page_content = " ".join([d.page_content for d in docs])

    # Configura o modelo de linguagem
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=openai_api_key,
    )

    # Cria o template de prompt para a consulta
    chat_template = ChatPromptTemplate.from_messages(
        [
            (
                "user",
                """Você é um assistente que responde perguntas sobre vídeos do YouTube baseado
                na transcrição do vídeo.

                Responda a seguinte pergunta: {pergunta}
                Procurando nas seguintes transcrições: {docs}

                Use somente a informação da transcrição para responder a pergunta. Se você não sabe, responda
                com "Eu não sei".

                Suas respostas devem ser bem detalhadas e verbosas.
                """,
            )
        ]
    )

    # Cria a cadeia de consulta usando o modelo de linguagem e o prompt
    chain = LLMChain(llm=llm, prompt=chat_template, output_key="answer")

    # Executa a cadeia com a pergunta e os documentos
    response = chain({"pergunta": query, "docs": docs_page_content})

    return response, docs

# %%
# Executa o script principal
if __name__ == "__main__":
    # Carrega a transcrição completa do vídeo do YouTube
    transcript = load_transcript("https://www.youtube.com/watch?v=Nu5gyrpaivE")

    # Imprime a transcrição completa
    print("Transcrição Completa:")
    for doc in transcript:
        print(doc.page_content)

    # Cria a base de vetores FAISS a partir da transcrição
    db = create_vector_from_transcript(transcript)

    # Consulta a base de vetores para obter uma resposta
    response, docs = get_response_from_query(
        db, "O que é falado sobre controle de preços?"
    )

    # Imprime a resposta
    print("Resposta à consulta:")
    print(response)
