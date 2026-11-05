import streamlit as st

# This file is the entry point. It lists the app's pages and runs the one
# the user picks from the sidebar. Lab 2 is the default page.

lab2_page = st.Page("Lab2.py", title="Lab 2: PDF Summarizer", default=True)
lab1_page = st.Page("Lab1.py", title="Lab 1: Document Q&A")
tip_calculator_page = st.Page("tip_calculator.py", title="Tip Calculator")

page = st.navigation([lab2_page, lab1_page, tip_calculator_page])
page.run()
