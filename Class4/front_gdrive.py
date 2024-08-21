import streamlit as st
import ts_videos_gdrive as lch
import os

# Dicionário para armazenar transcrições por ID de arquivo
transcription_cache = {}

# Configuração da página
st.set_page_config(
    page_title="ScriptoHub - Google Drive Edition",
    page_icon="🎥",
    layout="centered",  # Centralizado para se assemelhar ao layout do Google
    initial_sidebar_state="collapsed",
)

# Estilo inspirado na página inicial do Google
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Product+Sans&display=swap');

    body {
        background-color: #FFFFFF;
        font-family: 'Product Sans', sans-serif;
    }
    .main-title {
        font-size: 3em;
        text-align: center;
        font-family: 'Product Sans', sans-serif;
        margin-top: 50px;
        letter-spacing: 2px;
    }
    .main-title span:nth-child(1) { color: #4285F4; } /* G - Azul */
    .main-title span:nth-child(2) { color: #EA4335; } /* o - Vermelho */
    .main-title span:nth-child(3) { color: #FBBC05; } /* o - Amarelo */
    .main-title span:nth-child(4) { color: #4285F4; } /* g - Azul */
    .main-title span:nth-child(5) { color: #34A853; } /* l - Verde */
    .main-title span:nth-child(6) { color: #EA4335; } /* e - Vermelho */
    .search-box {
        display: flex;
        justify-content: center;
        margin-top: 40px;
    }
    .search-input {
        width: 60%;
        padding: 15px;
        border: 1px solid #dfe1e5;
        border-radius: 24px;
        font-size: 16px;
        outline: none;
        box-shadow: 0 1px 6px rgba(32, 33, 36, 0.28);
        transition: box-shadow 0.3s;
    }
    .search-input:focus {
        box-shadow: 0 1px 6px rgba(32, 33, 36, 0.35);
    }
    .buttons {
        display: flex;
        justify-content: center;
        margin-top: 30px;
    }
    .stButton button {
        background-color: #4285F4;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        margin: 0 10px;
        transition: background-color 0.3s;
    }
    .stButton button:hover {
        background-color: #3367D6;
    }
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 50px;
        font-size: 0.9em;
        color: #555555;
        border-top: 1px solid #CCCCCC;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Título principal, estilo Google
st.markdown(
    "<div class='main-title'><span>S</span><span>c</span><span>r</span><span>i</span><span>p</span><span>t</span><span>o</span><span>Hub</span></div>",
    unsafe_allow_html=True,
)

# Caixa de pesquisa estilo Google
with st.form(key="search_form"):
    file_id = st.text_input("Google Drive File ID", placeholder="Enter Google Drive File ID...", key="file_id", label_visibility="collapsed")
    submit_button = st.form_submit_button(label="Get Full Transcript")

# Processamento do vídeo e transcrição
if submit_button and file_id:
    if file_id in transcription_cache:
        st.success("This video has already been transcribed. Here is the cached transcription.")
        formatted_transcription, file_name = transcription_cache[file_id]
    else:
        # Mostra um spinner enquanto processa o vídeo
        with st.spinner("Authenticating with Google Drive..."):
            service = lch.authenticate_gdrive()

        # Mostra uma mensagem de status para o download
        st.info("Downloading video from Google Drive...")
        video, file_name, duration = lch.download_video_from_gdrive(service, file_id)

        # Mostra o nome do arquivo e a duração
        st.write(f"**File Name:** {file_name}")
        st.write(f"**Duration:** {duration // 60} minutes and {duration % 60:.1f} seconds")

        # Mensagem de progresso de transcrição
        st.info("Transcribing video...")
        transcription = lch.transcribe_video(video)

        # Mensagem de progresso de formatação
        st.info("Formatting transcription...")
        formatted_transcription = lch.format_transcript(transcription)

        # Armazena a transcrição no cache
        transcription_cache[file_id] = (formatted_transcription, file_name)
        st.success("Transcription complete!")

    # Exibe a transcrição
    st.markdown("<h3 style='color: #4285F4;'>Full Transcript</h3>", unsafe_allow_html=True)
    st.text_area(label="Transcript", value=formatted_transcription, height=400, help="Review the transcribed content here.")

    # Gera o nome do arquivo para download
    transcript_file_name = f"{file_name.split('.')[0]}_transcript.txt"

    # Botão para download da transcrição
    st.download_button(
        label="Download Transcript",
        data=formatted_transcription,
        file_name=transcript_file_name,
        mime="text/plain",
    )

# Rodapé estilizado
st.markdown(
    """
    <div class="footer">
        © 2024 ScriptoHub - Google Drive Edition. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True,
)
