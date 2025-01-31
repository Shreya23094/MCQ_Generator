import os
import re
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_read
import streamlit as st
from src.mcqgenerator.MCQGenerator import generate_chain
from src.mcqgenerator.logger import logging


with open("Response.json") as file:
    RESPONSE_JSON=json.load(file)

#create title
st.title("MCQs Creator with HuggingFace and Langchain")

#Create a form using st.form
with st.form("user_inputs:"):
    uploaded_file=st.file_uploader("Upload a PDF or Text File")
    mcq_count=st.number_input("Number of MCQs",min_value=3,max_value=50)
    subject=st.text_input("Insert Subject",max_chars=30)
    tone=st.text_input("Complexity level of Questions",max_chars=20,placeholder="Simple")
    button=st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading..."):
            try:
                text=read_file(uploaded_file)
                response=generate_chain(
                    {
                        "text":text,
                        "number":mcq_count,
                        "subject":subject,
                        "tone":tone,
                        "response_json":json.dumps(RESPONSE_JSON)
                    }
                )
                #st.write(quiz)
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")
            else:
                quiz = re.findall(r">([^<]+)<", response['quiz'],re.DOTALL)
                quiz="\n\n".join(quiz)
                            
                if isinstance(quiz,str):
                    if quiz is not None:
                        st.write(quiz)
                    else:
                        st.error("Error in the data")
                else:
                    st.write(quiz)