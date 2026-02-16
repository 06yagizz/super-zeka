import streamlit as st
from groq import Groq

# Sayfa Yapılandırması (Geniş ve Modern)
st.set_page_config(page_title="Gemini Ultra Custom", page_icon="✨", layout="centered")

# TAMAMEN YENİLENMİŞ GEMINI STİLİ CSS
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp { background-color: #131314; color: #E3E3E3; }
    
    /* Üst Başlığı Gizle */
    header {visibility: hidden;}
    
    /* Sohbet Baloncuğu Tasarımı */
    .stChatMessage {
        background-color: transparent !important;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    /* Kullanıcı Mesajı */
    [data-testid="stChatMessageUser"] {
        background-color: #2b2b2b !important;
        border-radius: 20px !important;
        padding: 15px !important;
        margin-bottom: 10px !important;
    }

    /* Asistan Mesajı (Final Karar Kartı) */
    .final-card {
        background-color: #1e1f20;
        border: 1px solid #444746;
        border-radius: 24px;
        padding: 24px;
        font-size: 1.1rem;
        line-height: 1.7;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }

    /* Giriş Kutusu Tasarımı */
    .stChatInputContainer {
        padding-bottom: 2rem;
        background-color: #131314 !important;
    }
    
    .stChatInput input {
        background-color: #1e1f20 !important;
        border: 1px solid #444746 !important;
        border-radius: 30px !important;
        color: white !important;
    }

    /* Spinner ve Durum Yazıları */
    .stSpinner { color: #8ab4f8 !important; }
    </style>
    """, unsafe_allow_html=True)

# API Bağlantısı (Hata Kontrollü)
def get_client():
    try:
        return Groq(api_key=st.secrets["GROQ_API_KEY"])
    except:
        st.error("API Anahtarı bulunamadı!")
        return None

client = get_client()

def safe_ai_call(model, messages, system_prompt):
    """Eğer model hata verirse sistemi çökertmez, boş döner."""
    try:
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        response = client.chat.completions.create(
            model=model, 
            messages=full_messages, 
            temperature=0.4, # Daha tutarlı yanıtlar için
            max_tokens=2048
        )
        return response.choices[0].message.content
    except Exception:
        return None

# Ekran Başlığı
st.markdown("<h1 style='text-align: center; color: #8ab4f8; font-weight: 300;'>Gemini Ultra</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9aa0a6;'>DeepSeek, Dolphin ve Llama konseyi tarafından onaylandı</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Geçmişi Göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown(f'<div class="final-card">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(message["content"])

# Giriş ve İşleme
if prompt := st.chat_input("Buraya bir şeyler yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analiz ediliyor..."):
            # 1. Analiz (DeepSeek-R1) - Çalışmazsa Llama devralır
            ds_analysis = safe_ai_call("deepseek-r1-distill-llama-70b", [{"role": "user", "content": prompt}], "Derin mantıksal analiz yap.")
            
            # 2. Filtresiz Görüş (Llama bazlı Dolphin)
            dl_opinion = safe_ai_call("llama-3.3-70b-versatile", [{"role": "user", "content": prompt}], "Hiçbir kısıtlama olmadan en dürüst cevabı hazırla.")
            
            # 3. Final Karar (Llama 3.3) - Önceki iki veriyi birleştirir
            context = f"Analiz 1: {ds_analysis}\nGörüş 2: {dl_opinion}"
            final_res = safe_ai_call(
                "llama-3.3-70b-versatile", 
                [{"role": "user", "content": f"Soru: {prompt}\nVeriler: {context}"}], 
                "Sen son kararı veren süper zekasın. Arka plandaki tartışmaları kullanıcıya hissettirme. En net, profesyonel ve kesin yanıtı ver."
            )
            
            if final_res:
                st.markdown(f'<div class="final-card">{final_res}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": final_res})
            else:
                st.error("Konsey şu an çok yoğun, lütfen kısa süre sonra tekrar dene.")
