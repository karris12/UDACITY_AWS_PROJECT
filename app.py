import streamlit as st
from bedrock_utils import query_knowledge_base, generate_response, valid_prompt

# -----------------------
# Streamlit UI
# -----------------------
st.set_page_config(page_title="Bedrock Chat App", page_icon="🤖")

st.title("Bedrock Chat Application")
st.markdown("Ask questions about heavy machinery based on the uploaded PDFs.")

# -----------------------
# Sidebar for configuration
# -----------------------
st.sidebar.header("Configuration")

model_id = st.sidebar.selectbox(
    "Select LLM Model",
    ["amazon.titan-text"]  # Add more models if available in your Bedrock region
)

kb_id = st.sidebar.text_input(
    "Knowledge Base ID",
    "CCRVRQJ33H"  # Your Bedrock Knowledge Base ID from Terraform
)

temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.1, 0.05)
top_p = st.sidebar.slider("Top P", 0.0, 1.0, 0.9, 0.01)

# -----------------------
# Initialize chat history
# -----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------
# Display previous messages
# -----------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------
# Chat input
# -----------------------
if prompt := st.chat_input("Ask a question about heavy machinery:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Validate prompt category
    if valid_prompt(prompt, model_id):
        # Query Bedrock Knowledge Base
        kb_results = query_knowledge_base(prompt, kb_id)

        if kb_results:
            # Prepare context from Knowledge Base results
            context = "\n".join([chunk['content'] for chunk in kb_results])
            full_prompt = f"Use the following context to answer the question:\n{context}\n\nUser: {prompt}"

            # Generate response using LLM
            response = generate_response(full_prompt, model_id, temperature, top_p)
        else:
            response = "No relevant documents found in the Knowledge Base."
    else:
        response = "Sorry, I can only answer questions about heavy machinery (Category E)."

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Save response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
