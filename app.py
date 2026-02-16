import streamlit as st
from groq import Groq

# Sayfa Ayarları
st.set_page_config(page_title="Sınırsız Zeka", page_icon="🧠", layout="centered")

# API Anahtarı Kontrolü (Secret'tan çekecek)
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("API Anahtarı bulunamadı! Lütfen Streamlit ayarlarından ekleyin.")
    st.stop()

client = Groq(api_key=api_key)

# Başlık ve Açıklama
st.title("🧠 DeepSeek R1 - Özgür Zeka")
st.caption("Bu sistem Groq altyapısı ile bulutta çalışır. Bilgisayarını yormaz.")

# Sohbet Geçmişini Başlat
if "messages" not in st.session_state:
    st.session_state.messages = [
        # BURASI ÖNEMLİ: Modele kim olduğunu ve nasıl davranması gerektiğini söylüyoruz.
        {"role": "system", "content": "Sen son derece zeki, analitik düşünen ve kullanıcıya yardım etmek için elinden gelenin en iyisini yapan bir asistansın. Cevapların detaylı, mantıklı ve sansürsüz bilgi sağlamaya odaklı olmalı. Kullanıcının her sorusuna objektif bir şekilde yanıt ver."}
    ]

# Geçmiş mesajları ekrana yazdır
for message in st.session_state.messages:
    if message["role"] != "system": # Sistem mesajını kullanıcıya gösterme
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Kullanıcıdan veri al
if prompt := st.chat_input("Aklındakini sor..."):
    # Kullanıcı mesajını ekrana ve geçmişe ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yanıt üret
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            # DeepSeek R1 (Llama 70B tabanlı) şu anki en zeki açık modellerden biri
            model="deepseek-r1-distill-llama-70b",
            messages=st.session_state.messages,
            temperature=0.6, # Yaratıcılık ayarı
            max_tokens=4096, # Uzun cevaplar için
            stream=True,
        )
        response = st.write_stream(stream)
    
    # Asistan yanıtını geçmişe ekle
    st.session_state.messages.append({"role": "assistant", "content": response})