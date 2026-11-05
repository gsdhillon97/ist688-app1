import streamlit as st
from openai import OpenAI, AuthenticationError, OpenAIError
from pypdf import PdfReader

# 1. Add a title to the web page
st.title("Lab 2: PDF Summarizer")
st.write("Upload a PDF (or .txt) document and OpenAI will summarize it.")

# 2. Get the OpenAI API key from Streamlit secrets
# Locally the key lives in .streamlit/secrets.toml (which Git ignores).
# On Streamlit Community Cloud it lives in the app's Settings > Secrets.
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except (KeyError, FileNotFoundError):
    api_key = ""

# 3. Sidebar options: summary type, language, and model
summary_type = st.sidebar.selectbox(
    "Type of summary",
    [
        "Summarize the document in 100 words",
        "Summarize the document in 2 connecting paragraphs",
        "Summarize the document in 5 bullet points",
    ],
)

language = st.sidebar.selectbox(
    "Language",
    ["English", "Spanish", "French", "German", "Chinese", "Hindi"],
)

# The mini model is the default (it is listed first).
# Summarizing is a fairly easy task, so the mini model's quality is good
# enough, and it costs about 100 times less than the flagship model.
models = {
    "Mini (gpt-6-luna)": "gpt-6-luna",
    "Flagship (gpt-6-astra)": "gpt-6-astra",
}
model_label = st.sidebar.selectbox("Model", list(models.keys()))
model = models[model_label]

# 4. Let the user upload a document
uploaded_file = st.file_uploader("Upload a document (.pdf or .txt)", type=["pdf", "txt"])

# 5. As soon as there is a document, summarize it
if uploaded_file is not None:
    # Read the document's text
    if uploaded_file.name.lower().endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        document = ""
        for page in reader.pages:
            document += (page.extract_text() or "") + "\n"
    else:
        document = uploaded_file.read().decode("utf-8")

    if not document.strip():
        st.error("Could not find any text in that document.")
        st.stop()

    if not api_key:
        st.error(
            "No OpenAI API key found. Add OPENAI_API_KEY to .streamlit/secrets.toml "
            "(or to the app's Secrets on Streamlit Community Cloud)."
        )
        st.stop()

    # The summary type and language are part of the instructions to the LLM
    instructions = f"{summary_type}. Write the summary in {language}."

    client = OpenAI(api_key=api_key)

    try:
        with st.spinner("Summarizing..."):
            response = client.responses.create(
                model=model,
                instructions=instructions,
                input=document,
            )

        # 6. Display the summary
        st.subheader("Summary")
        st.write(response.output_text)
    except AuthenticationError:
        st.error("OpenAI did not accept the API key in your secrets. Check it and try again.")
    except OpenAIError as error:
        st.error(f"Something went wrong talking to OpenAI: {error}")
