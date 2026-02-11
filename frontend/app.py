import streamlit as st
import requests

# 1. Page Configuration: Must be "wide" to support an 80/20 layout properly
st.set_page_config(page_title="Video to Doc AI", layout="wide")

# The URL where your FastAPI server is running
API_URL = "http://localhost:8000"

# 2. Initialize Session State
# We need to remember the processed document and chat history between button clicks
if "doc_hash" not in st.session_state:
    st.session_state.doc_hash = None
if "documentation" not in st.session_state:
    st.session_state.documentation = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🎥 Video to Structured Documentation")

# 3. Input Section (Top)
with st.container():
    st.markdown("### Upload a video or paste a link")
    input_type = st.radio("Choose Input Type:", ["Video Link (YouTube, Vimeo, etc.)", "File Upload"], horizontal=True)
    
    url_input = None
    file_input = None
    
    if input_type == "Video Link (YouTube, Vimeo, etc.)":
        url_input = st.text_input("Paste the video URL here:")
    else:
        file_input = st.file_uploader("Upload an audio or video file", type=["mp4", "mp3", "wav", "mkv", "mov"])
        
    if st.button("Generate Documentation", type="primary"):
        if not url_input and not file_input:
            st.warning("Please provide a link or upload a file first.")
        else:
            with st.spinner("Extracting audio, transcribing, and generating notes... This might take a minute."):
                try:
                    # Prepare the payload for FastAPI
                    data = {}
                    files = {}
                    if url_input:
                        data = {"url": url_input}
                    elif file_input:
                        files = {"file": (file_input.name, file_input.getvalue(), file_input.type)}
                    
                    # Call the /process endpoint
                    response = requests.post(f"{API_URL}/process", data=data, files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        # Save the results to session state
                        st.session_state.doc_hash = result["hash"]
                        st.session_state.documentation = result["documentation"]
                        st.session_state.chat_history = [] # Reset chat for a new video
                    else:
                        st.error(f"Backend Error: {response.text}")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {e}")

st.divider()

# 4. The 80/20 Layout Section
if st.session_state.documentation and st.session_state.doc_hash:
    
    # Create the column split: 8 parts for the doc, 2 parts for the chat
    doc_col, chat_col = st.columns([8, 2], gap="large")
    
    # --- LEFT SIDE: 80% Documentation ---
    with doc_col:
        st.subheader("📚 Generated Notes")
        with st.container(height=600):  # Fixed height with scrollbar
            st.markdown(st.session_state.documentation)
            
    # --- RIGHT SIDE: 20% RAG Chatbot ---
    with chat_col:
        st.subheader("💬 Ask the Video")
        
        # Display previous chat messages
        chat_container = st.container(height=500)
        with chat_container:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Chat input box stuck to the bottom of the column
        if prompt := st.chat_input("Ask a question about the notes..."):
            # 1. Show user message instantly
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)
            
            # 2. Call the RAG backend
            with chat_container:
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        chat_payload = {
                            "collection_name": st.session_state.doc_hash,
                            "query": prompt
                        }
                        chat_res = requests.post(f"{API_URL}/chat", json=chat_payload)
                        
                        if chat_res.status_code == 200:
                            answer = chat_res.json()["answer"]
                            st.markdown(answer)
                            st.session_state.chat_history.append({"role": "assistant", "content": answer})
                        else:
                            st.error("Error communicating with chat engine.")