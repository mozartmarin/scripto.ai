# %%
import streamlit as st
import transcript_videos as lch

# %%
# Título da aplicação
st.title("Assistente do Youtube - Transcrição Completa")

# %%
# Formulário na barra lateral para entrada de URL
with st.sidebar:
    with st.form(key="my_form"):
        youtube_url = st.sidebar.text_area(label="URL do Vídeo", max_chars=100)
        submit_button = st.form_submit_button(label="Gerar Transcrição")

# %%
# Verifica se o usuário forneceu a URL e então processa a transcrição
if youtube_url and submit_button:
    # Carrega a transcrição completa do vídeo
    transcript = lch.load_transcript(youtube_url)

    # Junta os trechos da transcrição
    full_transcript = "\n\n".join([doc.page_content for doc in transcript])

    # Exibe a transcrição completa estruturada
    st.subheader("Transcrição Completa:")
    st.markdown(full_transcript)
