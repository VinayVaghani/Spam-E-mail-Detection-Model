import re
import joblib
import streamlit as st
from email import policy
from email.parser import BytesParser

# -----------------------------
# UI THEME / CSS
# -----------------------------
st.set_page_config(page_title="Spam Email Detector", layout="centered")

CUSTOM_CSS = """
<style>
.stApp {
    background: radial-gradient(circle at 10% 10%, rgba(0, 255, 209, 0.10), transparent 30%),
                radial-gradient(circle at 90% 20%, rgba(255, 0, 128, 0.10), transparent 35%),
                radial-gradient(circle at 40% 90%, rgba(0, 112, 255, 0.10), transparent 35%);
}
.hero {
    padding: 1.2rem 1.2rem 1.0rem 1.2rem;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.14);
    background: rgba(20, 20, 20, 0.55);
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    margin-bottom: 1rem;
}
.hero h1 { margin: 0; font-size: 2rem; line-height: 1.1; }
.hero p { margin: 0.35rem 0 0; color: rgba(255,255,255,0.75); }
div[data-testid="stTextArea"] textarea,
div[data-testid="stFileUploader"] section,
div[data-testid="stTextInput"] input { border-radius: 14px !important; }
.badge {
    display: inline-block;
    padding: 0.15rem 0.55rem;
    border-radius: 999px;
    font-size: 0.85rem;
    border: 1px solid rgba(255,255,255,0.16);
    background: rgba(255,255,255,0.06);
    margin-right: 0.35rem;
}
.footer {
    margin-top: 1rem;
    padding: 0.8rem 1rem;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.12);
    color: rgba(255,255,255,0.72);
    background: rgba(20,20,20,0.35);
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.markdown(
    """
<div class="hero">
  <div>
    <span class="badge">⚡ Fast</span>
    <span class="badge">🧠 Notebook Model</span>
    <span class="badge">🔒 Local</span>
  </div>
  <h1>Spam Email Detector</h1>
</div>
""",
    unsafe_allow_html=True,
)

MODEL_PATH = "spam_model.pkl"

# -----------------------------
# Helpers
# -----------------------------
def clean_text(text: str) -> str:
    text = text or ""
    return re.sub(r"\s+", " ", text).strip()

def read_txt(uploaded_file) -> str:
    return uploaded_file.read().decode("utf-8", errors="ignore")

def read_eml(uploaded_file) -> str:
    raw = uploaded_file.read()
    if not raw:
        return ""
    msg = BytesParser(policy=policy.default).parsebytes(raw)
    parts = []
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = str(part.get("Content-Disposition", "")).lower()
            if ctype == "text/plain" and "attachment" not in disp:
                parts.append(part.get_content())
        if not parts:
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    parts.append(part.get_content())
    else:
        parts.append(msg.get_content())
    return "\n".join([p for p in parts if p])

# -----------------------------
# Session state init
# -----------------------------
st.session_state.setdefault("email_input", "")
st.session_state.setdefault("result", None)
st.session_state.setdefault("uploader_key", 0)
st.session_state.setdefault("clear_trigger", False)

# Apply clearing BEFORE widgets are created
if st.session_state.clear_trigger:
    st.session_state.email_input = ""
    st.session_state.result = None
    st.session_state.uploader_key += 1
    st.session_state.clear_trigger = False

@st.cache_resource(show_spinner=False)
def load_model():
    return joblib.load(MODEL_PATH)

try:
    model = load_model()
except Exception as e:
    st.error(
        f"❌ Could not load **{MODEL_PATH}**.\n\n"
        f"Make sure `spam_model.pkl` is in the same folder as `app.py`.\n\n"
        f"Error: {e}"
    )
    st.stop()


uploaded = st.file_uploader(
    "Upload email file (.txt or .eml)",
    type=["txt", "eml"],
    key=f"uploader_{st.session_state.uploader_key}"
)

if uploaded is not None:
    try:
        if hasattr(uploaded, "size") and uploaded.size == 0:
            uploaded = None
        else:
            if uploaded.name.lower().endswith(".txt"):
                st.session_state.email_input = clean_text(read_txt(uploaded))
            elif uploaded.name.lower().endswith(".eml"):
                st.session_state.email_input = clean_text(read_eml(uploaded))
            st.success(f"Loaded file: **{uploaded.name}**")
    except Exception:
        st.warning("File was cancelled or could not be read. Please upload again.")

st.text_area(
    "Or paste your email content here:",
    key="email_input",
    height=220,
    placeholder="Paste the full email message here..."
)

col1, col2 = st.columns([1, 1])
with col1:
    predict_btn = st.button("🔍 Predict", use_container_width=True)
with col2:
    clear_btn = st.button("🧹 Clear", use_container_width=True)

if clear_btn:
    st.session_state.clear_trigger = True
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()


if predict_btn:
    text = clean_text(st.session_state.email_input)
    if not text:
        st.session_state.result = {"type": "warning", "msg": "Please paste an email or upload a file first."}
    else:
        pred = int(model.predict([text])[0])
        proba = None
        if hasattr(model, "predict_proba"):
            proba = float(model.predict_proba([text])[0][1])
        st.session_state.result = {"type": "spam" if pred == 1 else "ham", "proba": proba}

res = st.session_state.result
if res:
    if res["type"] == "warning":
        st.warning(res["msg"])
    elif res["type"] == "spam":
        st.error("🚨 Result: **SPAM EMAIL**")
        if res.get("proba") is not None:
            st.progress(min(max(res["proba"], 0.0), 1.0))
            st.write(f"Spam probability: **{res['proba']*100:.2f}%**")
    else:
        st.success("✅ Result: **NOT SPAM**")
        if res.get("proba") is not None:
            st.progress(min(max(res["proba"], 0.0), 1.0))
            st.write(f"Spam probability: **{res['proba']*100:.2f}%**")

st.markdown(
    """
""",
    unsafe_allow_html=True,
)
