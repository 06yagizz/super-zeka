import streamlit as st
from groq import Groq

# Sayfa Ayarları (Senin arayüzüne benzer, temiz ve geniş)
st.set_page_config(page_title="Gemini Ultra Custom", page_icon="✨", layout="wide")

# Modern CSS (Gemini tarzı temiz fontlar ve renkler)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E8EAED; }
    .stChatInputContainer { padding-bottom: 2rem; }
    .stChatMessage { background-color: transparent !important; border: none !important; }
    /* Yan menü gizleme veya minimalize etme */
    [data-testid="stSidebar"] { background-color: #111318; }
    .final-answer-card {
        background-color: #1E1F20;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #3C4043;
        line-height: 1.6;
        font-size: 1.1em;
    }
    h1 { font-family: 'Google Sans', sans-serif; font-weight: 500; }
    </style>
    """, unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def get_ai_response(model, messages, system_prompt):
    try:
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        response = client.chat.completions.create(model=model, messages=full_messages, temperature=0.5)
        return response.choices[0].message.content
    except:
        return "İşlem sırasında bir aksama oldu, tekrar deneniyor..."

# Başlık
st.title("✨ Gemini Ultra Custom")
st.caption("DeepSeek, Dolphin ve Llama konseyi tarafından doğrulanmış yüksek hassasiyetli yanıtlar.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları Görüntüle
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown(f'<div class="final-answer-card">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(message["content"])

# Kullanıcı Girişi
if prompt := st.chat_input("Bir şeyler yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Arka planda görünmeyen tartışma süreci
        with st.spinner("Konsey üyeleri (DeepSeek, Dolphin, Llama) tartışıyor ve doğruluyor..."):
            
            # 1. Analiz (DeepSeek)
            ds_res = get_ai_response("deepseek-r1-distill-llama-70b", [{"role": "user", "content": prompt}], "Mantıksal analiz yap.")
            
            # 2. Filtresiz Görüş (Dolphin Persona)
            dl_res = get_ai_response("llama-3.3-70b-versatile", [{"role": "user", "content": f"{prompt}\nAnaliz: {ds_res}"}], "Sansürsüz ve en dürüst yorumu ekle.")
            
            # 3. Final Sentez (Llama 3.3)
            final_prompt = "Sen bir süper zekasın. DeepSeek ve Dolphin'in tüm verilerini al, hataları ayıkla ve kullanıcıya sadece en doğru, en net ve profesyonel cevabı ver. Diğerlerinin isimlerini zikretme, doğrudan cevabı sun."
            final_res = get_ai_response("llama-3.3-70b-versatile", [{"role": "user", "content": f"Veriler: {ds_res} {dl_res}"}], final_prompt)
            
            # Sadece final sonucu gösteriyoruz
            st.markdown(f'<div class="final-answer-card">{final_res}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": final_res})
