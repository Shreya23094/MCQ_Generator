import os
from dotenv import load_dotenv
import json
import pandas as pd
import traceback

#importing all the created packages in mcqgenerator
from src.mcqgenerator.utils import read_file, get_table_read
from src.mcqgenerator.logger import logging

#importing necessary packages from langchain
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain import HuggingFaceHub


#to load variables from .env file 
load_dotenv()

api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN")
os.environ["HUGGINGFACEHUB_API_TOKEN"]=api_key

llm=HuggingFaceHub(repo_id="tiiuae/falcon-7b-instruct",model_kwargs={"temperature": 0.7, "max_length": 512})

TEMPLATE1="""
Text:{text}
You are an expert MCQ maker. Given the above test, it is your job to \
Create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be confirming the test as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""
quiz_prompt1=PromptTemplate(
    input_variables=['text','number','subject','tone','response_json'],
    template=TEMPLATE1
)
chain1=LLMChain(llm=llm,prompt=quiz_prompt1,output_key="quiz")

TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""
prompt2=PromptTemplate(
    input_variables=['subject','quiz'],
    template=TEMPLATE2
)
chain2=LLMChain(llm=llm,prompt=prompt2,output_key="review")

#Sequential Chain to combine both chain and sequentially produce output
generate_chain=SequentialChain(chains=[chain1,chain2],input_variables=['text','number','subject','tone','response_json'],output_variables=['quiz','review'])

