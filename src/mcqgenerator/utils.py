import os
import PyPDF2
import json
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdfFileReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
        except Exception as e:
            raise Exception("error loading the pdf")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        raise Exception(
            "unsupported file format"
        )
    
# def get_table_data(quiz_str):
#     try:
#         print(quiz_str)
#         quiz_dict=json.loads(quiz_str)
#         quiz_table_data=[]
#         for key,value in quiz_dict.items():
#             mcq=value["mcq"]
#             option=" || ".join(
#                 [
#                     f"{option}->{option-value}"
#                     for option,option_value in value["option"].items()
#                     ]
#             )
#             correct=value["correct"]
#             quiz_table_data.append({"MCQ":mcq,"choices":option,"correct":correct})
#         return quiz_table_data
#     except Exception as e:
#         traceback.print_exception(type(e),e,e.__traceback__)
#         return False

import json

def get_table_data(quiz_str):
    if not quiz_str or not quiz_str.strip():
        print("Error: quiz_str is empty")
        return []

    try:
        quiz_dict = json.loads(quiz_str)
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        return []

    table_data = []
    for q_no, q_data in quiz_dict.items():
        options_dict = q_data.get("option", {})
        choices_combined = " || ".join(
            [f"{opt}->{opt_val}" for opt, opt_val in options_dict.items()]
        )
        row = {
            "Q.No": q_no,
            "Question": q_data.get("mcq", ""),
            "Option A": options_dict.get("a", ""),
            "Option B": options_dict.get("b", ""),
            "Option C": options_dict.get("c", ""),
            "Option D": options_dict.get("d", ""),
            "Choices": choices_combined,
            "Correct": q_data.get("correct", "")
        }
        table_data.append(row)

    return table_data
