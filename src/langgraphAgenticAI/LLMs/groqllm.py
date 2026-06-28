import os
from langchain_groq import ChatGroq
import streamlit as st

class GroqLLM:
    def __init__(self, user_controls_inputs):
        self.user_control_inputs = user_controls_inputs

    def get_llm_models(self):
        try:
            groq_api_key = self.user_control_inputs["GROQ_API_KEY"]
            selected_groq_model = self.user_control_inputs["selected_groq_model"]
            if groq_api_key == '' and os.environ["GROQ_API_KEY"] == '':
                st.error("Please enter the GROQ API key")

            llm = ChatGroq(api_key=groq_api_key, model=selected_groq_model)

        except Exception as e:
            raise ValueError(f"Error occured with exception: {e}")
        return llm
    