from dotenv import load_dotenv
import os
import openai

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")