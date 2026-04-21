from flask import Flask, render_template, jsonify, request, Response, stream_with_context
from src.helper import download_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)
load_dotenv()

# Environment Variables চেক করা
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not PINECONE_API_KEY or not OPENAI_API_KEY:
    raise ValueError("API Keys are missing in Environment Variables!")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Initialization
embeddings = download_embeddings()
index_name = "medical-chatbot"

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

chatModel = ChatOpenAI(model="gpt-4o")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form.get("msg")
    if not msg:
        return "Message is empty", 400
    
    @stream_with_context
    def generate():
        try:
            for chunk in rag_chain.stream({"input": msg}):
                if 'answer' in chunk:
                    yield chunk['answer']
        except Exception as e:
            yield f"\nError: {str(e)}"

    return Response(generate(), mimetype='text/plain')

# app.py এর একদম শেষে এই অংশটুকু রাখুন
if __name__ == '__main__':
    # host="0.0.0.0" মাস্ট, নাহলে কন্টেইনারের বাইরে থেকে এক্সেস পাওয়া যাবে না
    # debug=False মাস্ট, প্রোডাকশনের সিকিউরিটির জন্য
    app.run(host="0.0.0.0", port=8080, debug=False)
