import streamlit as st

# This file is the entry point. It lists the app's pages and runs the one
# the user picks from the sidebar.

tip_calculator_page = st.Page("tip_calculator.py", title="Tip Calculator")
document_qa_page = st.Page("document_qa.py", title="Document Q&A")

page = st.navigation([tip_calculator_page, document_qa_page])
page.run()
