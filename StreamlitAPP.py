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


with open("C:\\Users\\SHREYA SINGH\\OneDrive\\Desktop\\MCQ_Generator\\Response.json") as file:
    RESPONSE_JSON=json.load(file)

#create title
st.title("MCQs Creator with HuggingFace and Langchain")

#Create a form using st.form
with st.form("user_inputs:"):
    uploaded_file=st.file_uploader("Upload a PDF or Text File")
    mcq_count=st.number_input("Number of MCQs",min_value=3,max_value=50)
    subject=st.text_input("Insert Subject",max_chars=50)
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
                match = re.search(r"### RESPONSE_JSON\s*(\{.*\})", response['quiz'], re.DOTALL)
                response_text=str(match.group(1))
                match = re.search(r"###\s*\w+:\s*\n(.*)", response_text, re.DOTALL)
                quiz=json.loads(str(match.group(1)))
                #st.write(quiz)
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")
            else:
                if isinstance(quiz,dict):
                    if quiz is not None:
                        table_data=get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                            t="Check from an expert English Writer of the above quiz:"
                            match=re.search(re.escape(t) + r"\s*(.*)",response['review'],re.DOTALL)
                            review=match.group(1)
                            st.text_area(label="Review",value=review)
                        else:
                            st.error("Error in the table data")
                else:
                    st.write(quiz)