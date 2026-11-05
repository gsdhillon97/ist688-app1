import streamlit as st
from openai import OpenAI, AuthenticationError, OpenAIError

# 1. Add a title to the web page
st.title("My Document Q&A")
st.write("Upload a .txt document, ask a question about it, and OpenAI will answer.")

# 2. Get the user's OpenAI API key
# type="password" hides the key on screen. The key is only used for this
# request. It is never saved, printed, or written into the code.
api_key = st.text_input("OpenAI API key", type="password")

# 3. Let the user upload a .txt document
uploaded_file = st.file_uploader("Upload a document (.txt)", type="txt")

# 4. Let the user ask a question about the document
question = st.text_input("Ask a question about the document")

# 5. When the button is clicked, send the document and question to OpenAI
if st.button("Get answer"):
    if not api_key:
        st.error("Please enter your OpenAI API key.")
    elif uploaded_file is None:
        st.error("Please upload a .txt document.")
    elif not question:
        st.error("Please enter a question.")
    else:
        # Read the uploaded file as text
        document = uploaded_file.read().decode("utf-8")

        client = OpenAI(api_key=api_key)

        try:
            with st.spinner("Thinking..."):
                response = client.responses.create(
                    model="gpt-6-luna",
                    instructions="Answer the question using only the document provided.",
                    input=f"Document:\n{document}\n\nQuestion: {question}",
                )

            # 6. Display the answer
            st.subheader("Answer")
            st.write(response.output_text)
        except AuthenticationError:
            st.error("OpenAI did not accept that API key. Check it and try again.")
        except OpenAIError as error:
            st.error(f"Something went wrong talking to OpenAI: {error}")
