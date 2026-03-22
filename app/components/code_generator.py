from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from .prompt_templates import build_test_case_to_java_code_prompt
from dotenv import load_dotenv
from config.settings import settings

LLM_MODEL = settings.LLM_MODEL
load_dotenv()

def generate_java_code(test_steps, context_chunks, placeholder=None):
    context = "\n---\n".join(context_chunks)

    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=0.3,
        streaming=True
    )
    
    prompt = build_test_case_to_java_code_prompt(test_steps, context)

    message = HumanMessage(content=prompt)

    java_code = ""
    stream = llm.stream([message])

    for chunk in stream:
        java_code += chunk.content
        if placeholder:
            placeholder.code(java_code, language="java")

    return java_code.strip()
