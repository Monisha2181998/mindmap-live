import gradio as gr
from database import save_note, get_all_notes
from nlp_extractor import extract_concepts
from knowledge_graph import add_note_to_graph, find_connections, get_graph_summary, rebuild_graph_from_db
from llm_connector import explain_connections, generate_daily_summary

# Rebuild graph from existing notes on startup
rebuild_graph_from_db()

def add_note(note_text):
    """Main function — process a new note"""
    
    if not note_text.strip():
        return "Please write something!", "", "", format_all_notes()
    
    # Step 1 — Extract concepts
    concepts = extract_concepts(note_text)
    if not concepts:
        concepts = ["general"]
    
    # Step 2 — Get previous notes to find connections
    previous_notes = get_all_notes()
    
    # Step 3 — Find connections to previous notes
    connections = find_connections(concepts, previous_notes)
    
    # Step 4 — Save note to database
    save_note(note_text, concepts)
    
    # Step 5 — Add to knowledge graph
    add_note_to_graph(note_text, concepts)
    
    # Step 6 — Ask LLM to explain connections
    explanation = explain_connections(note_text, connections)
    
    # Step 7 — Graph summary
    summary = get_graph_summary()
    graph_info = f"Your knowledge map has {summary['total_nodes']} nodes and {summary['total_edges']} connections\n\n"
    graph_info += f"Concepts explored so far:\n{', '.join(summary['concepts'])}"
    
    # Format concepts
    concepts_text = "Concepts found: " + ", ".join(concepts)
    
    return concepts_text, explanation, graph_info, format_all_notes()

def format_all_notes():
    """Format all notes for display"""
    notes = get_all_notes()
    if not notes:
        return "No notes yet. Add your first note above!"
    
    formatted = ""
    for note in reversed(notes):
        formatted += f"📅 {note.timestamp.strftime('%B %d, %Y — %H:%M')}\n"
        formatted += f"📝 {note.content}\n"
        formatted += f"🏷️  {note.concepts}\n"
        formatted += "─" * 50 + "\n"
    
    return formatted

def get_summary():
    """Generate daily summary of all notes"""
    notes = get_all_notes()
    if not notes:
        return "No notes yet. Start adding your thoughts!"
    return generate_daily_summary(notes)

# Build Gradio UI
with gr.Blocks(title="MindMap Live") as app:
    
    gr.Markdown("""
    # 🧠 MindMap Live
    ### Your personal knowledge graph — turns daily notes into connected insights
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            note_input = gr.Textbox(
                label="💭 What's on your mind today?",
                placeholder="Type your note, idea, or what you learned today...",
                lines=4
            )
            add_btn = gr.Button("➕ Add Note", variant="primary", size="lg")
        
        with gr.Column(scale=1):
            gr.Markdown("### How it works")
            gr.Markdown("""
            1. Type any note or idea
            2. AI extracts key concepts
            3. Finds connections to past notes
            4. Explains the connections
            5. Grows your knowledge map
            """)
    
    with gr.Row():
        concepts_out = gr.Textbox(label="🏷️ Concepts extracted", interactive=False)
    
    with gr.Row():
        with gr.Column():
            explanation_out = gr.Textbox(
                label="🔗 Connections found",
                interactive=False,
                lines=5
            )
        with gr.Column():
            graph_out = gr.Textbox(
                label="🗺️ Your knowledge map",
                interactive=False,
                lines=5
            )
    
    gr.Markdown("---")
    
    summary_btn = gr.Button("📊 Generate my daily summary", variant="secondary")
    summary_out = gr.Textbox(label="📊 Daily summary", interactive=False, lines=5)
    
    gr.Markdown("---")
    gr.Markdown("### 📚 All your notes")
    notes_display = gr.Textbox(
        label="",
        value=format_all_notes(),
        interactive=False,
        lines=15
    )
    
    # Connect buttons
    add_btn.click(
        fn=add_note,
        inputs=[note_input],
        outputs=[concepts_out, explanation_out, graph_out, notes_display]
    )
    
    summary_btn.click(
        fn=get_summary,
        inputs=[],
        outputs=[summary_out]
    )

if __name__ == "__main__":
    app.launch(share=True, theme=gr.themes.Soft())