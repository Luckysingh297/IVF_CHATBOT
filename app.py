import streamlit as st
from uuid import uuid4
from rag_chain import ask_question

# ---------------------------------
# Page Config
# ---------------------------------
st.set_page_config(
    page_title="IVF AI Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------
# Session State
# ---------------------------------
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True

if "chats" not in st.session_state:
    chat_id = str(uuid4())
    st.session_state.chats = {chat_id: []}
    st.session_state.active_chat = chat_id

# ---------------------------------
# CSS (POLISHED)
# ---------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a);
}

/* Chat bubbles */
.user {
    background:#2563eb;
    color:white;
    padding:14px;
    border-radius:14px;
    margin:10px 0;
    max-width:70%;
    margin-left:auto;
}
.bot {
    background:#e5e7eb;
    color:black;
    padding:14px;
    border-radius:14px;
    margin:10px 0;
    max-width:75%;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background:#0b1220;
}

/* Floating toggle */
.toggle-btn {
    position: fixed;
    top: 16px;
    left: 12px;
    z-index: 1000;
}
.toggle-btn button {
    border-radius: 8px;
    padding: 6px 10px;
    background:#1f2937;
    color:white;
    border:none;
}

/* Inputs */
input {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# Sidebar Toggle
# ---------------------------------
st.markdown('<div class="toggle-btn">', unsafe_allow_html=True)
if st.button("⏪" if st.session_state.sidebar_open else "⏩"):
    st.session_state.sidebar_open = not st.session_state.sidebar_open
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------
# Sidebar (Chat History)
# ---------------------------------
if st.session_state.sidebar_open:
    with st.sidebar:
        st.markdown("## 💬 Chat History")

        if st.button("➕ New Chat"):
            new_id = str(uuid4())
            st.session_state.chats[new_id] = []
            st.session_state.active_chat = new_id
            st.rerun()

        st.divider()

        for cid, msgs in list(st.session_state.chats.items()):
            title = msgs[0]["content"][:24] + "..." if msgs else "New chat"

            col1, col2 = st.columns([5, 1])

            if col1.button(title, key=f"load_{cid}"):
                st.session_state.active_chat = cid
                st.rerun()

            if col2.button("🗑️", key=f"del_{cid}"):
                del st.session_state.chats[cid]
                if not st.session_state.chats:
                    nid = str(uuid4())
                    st.session_state.chats[nid] = []
                    st.session_state.active_chat = nid
                else:
                    st.session_state.active_chat = next(iter(st.session_state.chats))
                st.rerun()

# ---------------------------------
# Main Header
# ---------------------------------
st.markdown(
    "<h2 style='text-align:center;color:white'>🧬 IVF AI Assistant</h2>",
    unsafe_allow_html=True
)

# ---------------------------------
# Answer Mode (NO BULLET)
# ---------------------------------
mode = st.radio(
    "Answer Mode",
    ["Short", "Detailed"],   # ✅ Bullet removed
    horizontal=True
)

# ---------------------------------
# Chat Area
# ---------------------------------
chat = st.session_state.chats[st.session_state.active_chat]

if not chat:
    st.markdown(
        "<div class='bot'>Hello! Ask me anything about IVF.</div>",
        unsafe_allow_html=True
    )

for msg in chat:
    css = "user" if msg["role"] == "user" else "bot"
    st.markdown(f"<div class='{css}'>{msg['content']}</div>", unsafe_allow_html=True)

# ---------------------------------
# Input
# ---------------------------------
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your question here…")
    send = st.form_submit_button("Send")

if send and user_input:
    chat.append({"role": "user", "content": user_input})

    answer = ask_question(user_input, mode)

    # ❌ Hide hallucinations
    if "do not specify" in answer.lower():
        answer = "I’m sorry, the available medical sources don’t contain reliable information on this."

    chat.append({"role": "assistant", "content": answer})
    st.rerun()
