"""Build an inspectable page–concept graph from authorized JSONL chunks."""
import json
from pathlib import Path
import networkx as nx

CONCEPTS = (
    "reinforcement learning", "machine learning", "transformer", "attention", "embedding",
    "overfitting", "cross-validation", "regularization", "gradient descent",
    "loss function", "bayes filter", "kalman filter", "computer vision",
    "convolutional", "classification", "neural network", "optimization",
)

def build_graph(chunks):
    graph = nx.Graph()
    for i, chunk in enumerate(chunks):
        url, content = chunk['url'], chunk['text']
        name = f"page::{i}"
        graph.add_node(name, type='page', url=url, title=chunk.get('title', url), snippet=content[:700])
        found = [concept for concept in CONCEPTS if concept in content.lower()]
        for concept in found:
            graph.add_node(concept, type='concept', title=concept)
            graph.add_edge(name, concept, type='explains')
        for x, concept in enumerate(found):
            for other in found[x + 1:]:
                if graph.has_edge(concept, other):
                    graph[concept][other]['weight'] += 1
                else:
                    graph.add_edge(concept, other, type='cooccurs', weight=1)
    return graph

def load_chunks(path):
    with open(path, encoding='utf8') as handle:
        return [json.loads(line) for line in handle if line.strip()]

def save_graph(graph, path):
    path=Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(nx.node_link_data(graph)), encoding='utf8')

def load_graph(path):
    return nx.node_link_graph(json.loads(Path(path).read_text(encoding='utf8')))
