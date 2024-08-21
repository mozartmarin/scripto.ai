import streamlit as st
import ts_videos_azure as lch  # Certifique-se de que este módulo esteja no mesmo diretório

# Configuração da página
st.set_page_config(
    page_title="Azure-Inspired Interface - ScriptoHub Azure Edition",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilo inspirado no Azure
st.markdown(
    """
    <style>
    body {
        background-color: #FFFFFF;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main-header {
        background-color: #0078D4;
        color: #FFFFFF;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
        text-align: center;
    }
    .main-title {
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        color: #0078D4;
        font-size: 1.2em;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #F3F2F1;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .sidebar h3 {
        color: #0078D4;
        margin-bottom: 20px;
        font-size: 1.2em;
    }
    .stTextArea textarea {
        background-color: #FFFFFF;
        color: #333;
        border-radius: 5px;
        border: 1px solid #CCC;
        padding: 10px;
    }
    .stButton button {
        background-color: #0078D4;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: background-color 0.3s;
    }
    .stButton button:hover {
        background-color: #005A9E;
    }
    .footer {
        text-align: center;
        padding: 10px;
        margin-top: 20px;
        font-size: 0.9em;
        color: #666;
        border-top: 1px solid #0078D4;
    }
    .progress-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
    }
    .progress-bar {
        background-color: #0078D4;
        height: 20px;
        border-radius: 10px;
        transition: width 0.5s;
    }
    .progress-background {
        background-color: #F3F2F1;
        width: 100%;
        height: 20px;
        border-radius: 10px;
        overflow: hidden;
    }
    .recent-transcriptions {
        margin-top: 20px;
        padding: 10px;
        background-color: #F3F2F1;
        border-radius: 10px;
    }
    .recent-transcriptions h3 {
        color: #0078D4;
        font-size: 1.2em;
    }
    .recent-transcriptions ul {
        list-style-type: none;
        padding: 0;
    }
    .recent-transcriptions li {
        padding: 5px 0;
        border-bottom: 1px solid #DDD;
    }
    .recent-transcriptions li:last-child {
        border-bottom: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Cabeçalho principal
st.markdown(
    """
    <div class="main-header">
        <h1 class="main-title">ScriptoHub Azure Edition</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h2 class='subtitle'>Your Azure Video Transcript Assistant</h2>", unsafe_allow_html=True)

# Conteúdo da barra lateral
st.sidebar.markdown("<h3>Upload & Transcribe</h3>", unsafe_allow_html=True)
with st.sidebar:
    with st.form(key="my_form"):
        video_url = st.text_area(label="Video URL", max_chars=500, help="Enter the full URL of the video.")
        submit_button = st.form_submit_button(label="Get Full Transcript")

# Corpo principal
if video_url:
    with st.spinner("Transcribing video with Azure Video Index..."):
        # Simula progresso da transcrição
        for percent_complete in range(0, 101, 10):
            st.markdown(
                f"""
                <div class="progress-wrapper">
                    <div class="progress-background">
                        <div class="progress-bar" style="width: {percent_complete}%;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.sleep(0.1)  # Simula tempo de processamento
        
        # Faz a transcrição do vídeo usando o Azure
        transcription = lch.transcribe_video_azure(video_url)

        # Formata a transcrição
        formatted_transcription = lch.format_transcript(transcription)

        # Exibe a transcrição
        st.markdown("<h3 style='color: #0078D4;'>Full Transcript</h3>", unsafe_allow_html=True)
        st.text_area(label="Transcript", value=formatted_transcription, height=400, key="transcript_area", help="Review the transcribed content here.")

        # Gera o nome do arquivo para download
        transcript_file_name = f"transcript.txt"

        # Botão para download da transcrição
        st.download_button(
            label="Download Transcript",
            data=formatted_transcription,
            file_name=transcript_file_name,
            mime="text/plain",
        )

# Seção criativa para transcrições recentes
st.markdown(
    """
    <div class="recent-transcriptions">
        <h3>Recent Transcriptions</h3>
        <ul>
            <li>Video 1 - Completed</li>
            <li>Video 2 - Completed</li>
            <li>Video 3 - Completed</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

# Rodapé
st.markdown(
    """
    <div class="footer">
        © 2024 ScriptoHub Azure Edition. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True,
)
