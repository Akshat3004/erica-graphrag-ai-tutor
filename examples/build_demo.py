"""Generate a synthetic, independently written example corpus and graph."""
from pathlib import Path
from erica.graph import build_graph,save_graph

SAMPLES=[
 ('reinforcement-learning', 'Reinforcement learning is a method where an agent learns a policy by acting and receiving rewards. Learning from feedback helps adjust actions.'),
 ('transformer-attention', 'A transformer uses attention to weigh relevant context tokens. Embedding vectors represent text numerically.'),
 ('model-validation', 'Overfitting occurs when model performance on training data exceeds generalization. Cross-validation assesses held-out performance. Regularization can reduce overfitting.'),
 ('optimization', 'Gradient descent adjusts parameters using derivatives of a loss function and a learning rate. Optimization seeks to reduce the loss function.'),
 ('bayes-filter', 'A Bayes filter estimates a hidden state by prediction and measurement updates. A Kalman filter is a special case for linear Gaussian systems.'),
 ('computer-vision', 'Computer vision analyzes images. Convolutional neural network architectures are often used for image classification.'),
]
if __name__=='__main__':
    chunks=[{'url':'https://example.org/demo/'+slug,'title':slug.replace('-',' ').title(),'text':text} for slug,text in SAMPLES]
    path=Path('erica/data/demo_graph.json')
    save_graph(build_graph(chunks),path)
    print('Saved',path,'with',len(chunks),'synthetic pages')
