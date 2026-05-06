import networkx as nx
from database import get_all_notes

G = nx.Graph()

def add_note_to_graph(note_content, concepts):
    # Unique ID for the note node
    note_node = f"NOTE: {note_content[:30]}..."
    G.add_node(note_node, type="note")
    
    for concept in concepts:
        G.add_node(concept, type="concept")
        G.add_edge(note_node, concept)
    
    # Connect concepts appearing in the same note to show relationships[cite: 5]
    for i, c1 in enumerate(concepts):
        for c2 in concepts[i+1:]:
            G.add_edge(c1, c2, weight=G.get_edge_data(c1, c2, {}).get("weight", 0) + 1)

def find_connections(new_concepts, previous_notes):
    found = []
    new_set = set([c.lower().strip() for c in new_concepts])
    
    for note in previous_notes:
        old_set = set([c.lower().strip() for c in note.concepts.split(",")])
        shared = new_set & old_set
        if shared:
            found.append({
                "old_note": note.content,
                "shared_concepts": list(shared),
                "timestamp": note.timestamp.strftime("%B %d")
            })
    return found

def rebuild_graph_from_db():
    global G
    G.clear()
    notes = get_all_notes()
    for note in notes:
        concepts = [c.strip() for c in note.concepts.split(",") if c.strip()]
        add_note_to_graph(note.content, concepts)

def get_graph_summary():
    concepts = [n for n, d in G.nodes(data=True) if d.get("type") == "concept"]
    return {
        "total_nodes": G.number_of_nodes(),
        "total_edges": G.number_of_edges(),
        "concepts": concepts
    }