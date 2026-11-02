"""Hybrid ranking and local graph context with conservative source reporting."""
import re
import networkx as nx
import numpy as np

def tokens(text):
    return set(re.findall(r'[a-z]+',text.lower()))

def cosine(left,right):
    a,b=np.asarray(left,dtype=float),np.asarray(right,dtype=float)
    if a.shape != b.shape or not a.size:return 0.
    norm=np.linalg.norm(a)*np.linalg.norm(b)
    return float(a@b/norm) if norm else 0.

def retrieve(graph, question, embed=None, top_k=5, radius=1):
    concepts=[node for node,data in graph.nodes(data=True) if data.get('type')=='concept']
    question_tokens=tokens(question)
    query_vector=None
    if embed is not None:
        try:query_vector=embed(question)
        except Exception:query_vector=None
    scored=[]
    for concept in concepts:
        overlap=len(question_tokens & tokens(concept))
        similarity=0.
        if query_vector is not None and graph.nodes[concept].get('embedding') is not None:
            similarity=max(0.,cosine(query_vector,graph.nodes[concept]['embedding']))
        score=0.3*overlap+similarity
        if score>0:scored.append((score,concept))
    matches=[c for _,c in sorted(scored,reverse=True)[:top_k]]
    sub=nx.Graph()
    for concept in matches:sub=nx.compose(sub,nx.ego_graph(graph,concept,radius=radius))
    pages=[];seen=set()
    for node,data in sub.nodes(data=True):
        if data.get('type')=='page' and data.get('url') not in seen:
            pages.append({'url':data['url'],'title':data.get('title',''), 'snippet':data.get('snippet','')})
            seen.add(data['url'])
    context='\n'.join(f"CONCEPT: {c}" for c in matches)+'\n'+ '\n'.join(f"PAGE: {p['title']}\nURL: {p['url']}\n{p['snippet']}" for p in pages[:15])
    return {'concepts':matches,'pages':pages,'context':context,'nodes':sub.number_of_nodes(),'edges':sub.number_of_edges()}
