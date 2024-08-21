import streamlit as st
import ts_videos as lch
import textwrap

st.title("Assistente do Youtube!")

with st.sidebar:
    with st.form(key="my_form"):
        youtube_url = st.text_area(label="URL do Vídeo", max_chars=100)
        submit_button = st.form_submit_button(label="Obter Transcrição Completa")

if youtube_url:
    # Obtém metadados do vídeo
    video_info = lch.get_video_metadata(youtube_url)
    
    # Exibe informações do vídeo
    st.subheader("Informações do Vídeo")
    st.text(f"Título: {video_info['title']}")
    st.text(f"Canal: {video_info['channel']}")
    st.text(f"Duração: {video_info['duration']} minutos")
    st.text(f"Publicado em: {video_info['publish_date']}")

    # Cria a base de vetores e obtém a transcrição
    db, transcript = lch.create_vector_from_yt_url(youtube_url)
    
    # Exibe a transcrição formatada
    st.subheader("Transcrição Completa")
    formatted_transcript = lch.format_transcript(transcript)
    st.text_area(label="Transcrição", value=formatted_transcript, height=300)

    # Botão para download da transcrição
    st.download_button(label="Baixar Transcrição", data=formatted_transcript, file_name="transcricao.txt")
