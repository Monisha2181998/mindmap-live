import networkx as nx
from database import get_all_notes
from nlp_extractor import extract_concepts

# Global graph
G = nx.Graph()

def add_note_to_graph(note_content, concepts):
    """Add a note and its concepts as nodes and edges to the graph"""
    
    # Add note node
    note_node = f"NOTE: {note_content[:30]}..."
    G.add_node(note_node, type="note")
    
    # Add concept nodes and connect to note
    for concept in concepts:
        G.add_node(concept, type="concept")
        G.add_edge(note_node, concept)
    
    # Connect concepts to each other within same note
    for i, c1 in enumerate(concepts):
        for c2 in concepts[i+1:]:
            if G.has_edge(c1, c2):
                # Strengthen existing connection
                G[c1][c2]["weight"] = G[c1][c2].get("weight", 1) + 1
            else:
                G.add_edge(c1, c2, weight=1)

def find_connections(new_concepts, previous_notes):
    """Find which new concepts appeared in previous notes"""
    connections = []
    
    for note in previous_notes:
        old_concepts = note.concepts.split(",")
        shared = set(new_concepts) & set(old_concepts)
        
        if shared:
            connections.append({
                "old_note": note.content,
                "shared_concepts": list(shared),
                "timestamp": note.timestamp.strftime("%B %d, %Y")
            })
    
    return connections

def get_graph_summary():
    """Return basic graph statistics"""
    return {
        "total_nodes": G.number_of_nodes(),
        "total_edges": G.number_of_edges(),
        "concepts": [n for n, d in G.nodes(data=True) if d.get("type") == "concept"]
    }

def rebuild_graph_from_db():
    """Rebuild graph from all saved notes on startup"""
    notes = get_all_notes()
    for note in notes:
        concepts = note.concepts.split(",")
        add_note_to_graph(note.content, concepts)
    print(f"Graph rebuilt with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

# Test it
if __name__ == "__main__":
    test_data = [
        ("I studied machine learning and neural networks", ["machine learning", "neural networks"]),
        ("Knowledge graphs store relationships between concepts", ["knowledge graphs", "relationships", "concepts"]),
        ("Machine learning uses neural networks for pattern recognition", ["machine learning", "neural networks", "pattern recognition"]),
    ]
    
    for content, concepts in test_data:
        add_note_to_graph(content, concepts)
    
    summary = get_graph_summary()
    print(f"Graph has {summary['total_nodes']} nodes and {summary['total_edges']} edges")
    print(f"Concepts in graph: {summary['concepts']}")
    
    # Test connection finding
    new_concepts = ["machine learning", "knowledge graphs"]
    print(f"\nFinding connections for: {new_concepts}")
    
    # Simulate previous notes
    class FakeNote:
        def __init__(self, content, concepts, timestamp):
            self.content = content
            self.concepts = concepts
            class T:
                def strftime(self, fmt): return "May 01, 2026"
            self.timestamp = T()
    
    fake_notes = [
        FakeNote("I studied machine learning", "machine learning,neural networks", None),
        FakeNote("Read about knowledge graphs", "knowledge graphs,relationships", None),
    ]
    
    connections = find_connections(new_concepts, fake_notes)
    for c in connections:
        print(f"Connected to note: '{c['old_note']}'")
        print(f"Shared concepts: {c['shared_concepts']}")
        print(f"Written on: {c['timestamp']}\n")