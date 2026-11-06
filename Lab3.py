import streamlit as st
from openai import OpenAI, AuthenticationError, OpenAIError

# 1. Add a title to the web page
st.title("Lab 3: Chatbot")
st.write("Chat with OpenAI. The chatbot remembers the conversation.")

# 2. Get the OpenAI API key from Streamlit secrets
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except (KeyError, FileNotFoundError):
    api_key = ""

if not api_key:
    st.error(
        "No OpenAI API key found. Add OPENAI_API_KEY to .streamlit/secrets.toml "
        "(or to the app's Secrets on Streamlit Community Cloud)."
    )
    st.stop()

client = OpenAI(api_key=api_key)

# 3. Conversation memory: st.session_state keeps the messages between reruns.
# Streamlit reruns this whole file every time the user sends a message, so
# without session_state the chatbot would forget everything each time.
greeting = {"role": "assistant", "content": "Hi! How can I help you?"}

if "messages" not in st.session_state:
    st.session_state.messages = [greeting]

# Refinement: a "Clear chat" button in the sidebar that starts a new
# conversation by resetting the memory back to just the greeting
if st.sidebar.button("Clear chat"):
    st.session_state.messages = [greeting]

# 4. Show every message so far
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Turn OpenAI's stream of events into a stream of text pieces,
# so st.write_stream can show the answer as it is being written
def text_pieces(stream):
    for event in stream:
        if event.type == "response.output_text.delta":
            yield event.delta


# 5. When the user sends a message, save it, then stream OpenAI's reply
prompt = st.chat_input("Type your message")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        with st.chat_message("assistant"):
            # Send the whole conversation, so OpenAI can see the earlier messages
            stream = client.responses.create(
                model="gpt-6-luna",
                input=st.session_state.messages,
                stream=True,
            )
            reply = st.write_stream(text_pieces(stream))

        # Save the reply so it is part of the memory for the next message
        st.session_state.messages.append({"role": "assistant", "content": reply})
    except AuthenticationError:
        st.error("OpenAI did not accept the API key in your secrets. Check it and try again.")
    except OpenAIError as error:
        st.error(f"Something went wrong talking to OpenAI: {error}")
