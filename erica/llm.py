"""Ollama API client. No credentials or source data are embedded."""
import os
import requests

BASE=os.environ.get('OLLAMA_BASE_URL','http://localhost:11434').rstrip('/')

def embed(text, model='nomic-embed-text'):
    response=requests.post(BASE+'/api/embed', json={'model':model,'input':text},timeout=35)
    response.raise_for_status()
    vectors=response.json().get('embeddings',[])
    return vectors[0] if vectors else None

def answer(prompt, model='qwen2.5:3b'):
    response=requests.post(BASE+'/api/generate',json={'model':model,'prompt':prompt,'stream':False,'options':{'temperature':0,'num_predict':350}},timeout=180)
    response.raise_for_status()
    return response.json().get('response','')
