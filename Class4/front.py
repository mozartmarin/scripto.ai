# %%
import streamlit as st
import langchain_helper as lch
import textwrap

# %%
# Título da aplicação
st.title("Assistente do Youtube!")

# %%
# Formulário na barra lateral para entrada de URL e consulta
with st.sidebar:
    with st.form(key="my_form"):
        youtube_url = st.sidebar.text_area(label="URL do Vídeo", max_chars=50)
        query = st.sidebar.text_area(
            label="Me pergunte sobre algo do vídeo!", max_chars=50, key="query"
        )
        submit_button = st.form_submit_button(label="Enviar")

# %%
# Verifica se o usuário forneceu a URL e a consulta, e então processa a resposta
if query and youtube_url:
    db = lch.create_vector_from_yt_url(youtube_url)
    response, docs = lch.get_response_from_query(db, query)

    # Exibe a resposta formatada
    st.subheader("Resposta:")
    st.text(textwrap.fill(response["answer"], width=85))
