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

import streamlit as st
from src.mcqgenerator.MCQgenerator import generate_evualuate_chain

with open('Response.json','r') as files:
    RESPONSE_JSON=json.load(files)

st.title("MCQ GENERATOR")


with st.form("user_input"):
    uploaded_file=st.file_uploader("upload file")
    mcq_coount=st.number_input("no. of mcq required",min_value=3,max_value=50)

    subject=st.text_input("Insert the subject",max_chars=30)
    tone=st.text_input("completion of question",max_chars=30,placeholder="simple")
    button=st.form_submit_button("Crate Mcqs")

if button and uploaded_file is not None and mcq_coount and subject and tone:
    with st.spinner("loading..."):
        try:
            text=read_file(uploaded_file)
            with get_openai_callback() as cb:
               response=generate_evualuate_chain(
                  {
            "text":text,
            "number":mcq_coount,
            "subject":subject,
            "tone":tone,
            "response_json":json.dumps(RESPONSE_JSON)
        }
               )
        except Exception as e:
            traceback.print_exception(type(e),e,e.__traceback__)
            st.error("error")
        
        else:
            print(f"Total tokens: {cb.total_tokens}")
        
        if isinstance(response,dict):
            quiz=response.get("quiz",None)
            if get_table_data is not None:
                df=pd.DataFrame(get_table_data(quiz))
                df.index=df.index+1
                st.table(df)
            else:
                st.error("Error in the table data")
        else:
            st.write(response)
