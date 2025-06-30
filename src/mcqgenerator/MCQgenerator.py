import os
import json
import pandas as pd
import traceback
from langchain_community.chat_models import ChatOpenAI
from langchain.llms import openai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback

from langchain.chains import SequentialChain

import PyPDF2
from src.mcqgenerator.utils import read_file,get_table_data
from dotenv import load_dotenv

load_dotenv()
key=os.getenv("api_key")
llm=ChatOpenAI(model="gpt-3.5-turbo",temperature=0.5) 

TEMPLATE="""
Text:{text}
you are a expert mcq generator.Given above is the text for which you have to generate a quiz of {number} mcq for {subject} in {tone} tone.Make sure that the questions are not repeated.
Make sure to format your response like RESPONSE_JSON_ below and use it as a guide.
{response_json}
"""

quiz_prompt_genrator=PromptTemplate(
    input_variables=["text","number","subject","tone","response_json"],
    template=TEMPLATE
)

quiz_chain=LLMChain(llm=llm,prompt=quiz_prompt_genrator,output_key="quiz",verbose=True)

TEMPLATE2="""
You are an expert english grammarian and writer.Given a multiple choice quiz for {subject} students.\you need to evaliiate the complexity of the question and give a complete analysis of the quiz.Only use at maax\
50 words for completion.If the quis not at per cognative analytical abilities of the students\ update the quiz question and change the tone such thatt.
Quiz_Mcqs:
{quiz} 
Return your final updated quiz in valid JSON format.

"""

review_chain=LLMChain(llm=llm,prompt=quiz_prompt_genrator,output_key="review",verbose=True)

generate_evualuate_chain=SequentialChain(chains=[quiz_chain,review_chain],input_variables=["text","number","subject","tone","response_json"],output_variables=["quiz","review"],verbose=True)
