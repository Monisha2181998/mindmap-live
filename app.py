import gradio as gr
import fitz  # PyMuPDF
from datetime import datetime
from database import save_note, get_all_notes, delete_note_by_id
from nlp_extractor import extract_concepts
from knowledge_graph import add_note_to_graph, find_connections, rebuild_graph_from_db, G
from llm_connector import explain_connections, generate_daily_summary
from graph_viz import create_timeline_graph
from notifier import send_summary_email

# Initialize the graph from the database
rebuild_graph_from_db()

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def get_dropdown_choices():
    # Uses .content to match your Note object structure
    return [f"{n.id}: {n.content[:30]}..." for n in get_all_notes()]

def format_all_notes_html():
    notes = get_all_notes()
    if not notes: 
        return "<p style='color:gray; text-align:center;'>Your research timeline is empty.</p>"
    
    html_out = "<div style='display: flex; flex-direction: column; gap: 10px; max-height: 400px; overflow-y: auto;'>"
    for note in reversed(notes):
        # Ensure concepts exist and split them into chips
        concepts_list = note.concepts.split(",") if note.concepts else []
        chips = "".join([
            f"<span style='background:rgba(127,119,221,0.1); color:#7f77dd; padding:2px 8px; border-radius:10px; margin-right:5px; font-size:0.7em; border:1px solid #7f77dd;'>{c.strip()}</span>" 
            for c in concepts_list if c.strip()
        ])
        
        html_out += f"""
        <div style='border-left: 4px solid #7f77dd; background:#161625; padding:12px; border-radius:8px;'>
            <p style='font-size:0.7em; opacity:0.5; margin:0;'>ID: {note.id} — {note.timestamp.strftime('%H:%M')}</p>
            <p style='margin:5px 0; color:white;'>{note.content[:200]}...</p>
            <div>{chips}</div>
        </div>
        """
    return html_out + "</div>"

def process_mixed_input(manual_text, files):
    status_updates = []
    last_explanation = ""
    
    # Handle Manual Text Input
    if manual_text and manual_text.strip():
        concepts = extract_concepts(manual_text)
        save_note(manual_text, concepts)
        rebuild_graph_from_db()
        # Find connections excluding the note just added
        last_explanation = explain_connections(manual_text, find_connections(concepts, get_all_notes()[:-1]))
        status_updates.append("✅ Manual note saved.")

    # Handle PDF Uploads
    if files:
        for file in files:
            raw_text = extract_text_from_pdf(file.name)
            # Create a clean entry for the database
            clean_text = f"Source: {file.name.split('\\')[-1]}\n\n{raw_text[:1500]}"
            concepts = extract_concepts(clean_text)
            save_note(clean_text, concepts)
            rebuild_graph_from_db()
            status_updates.append(f"✅ Processed PDF: {file.name.split('/')[-1]}")
        
        # Analyze connections for the batch of uploaded files
        last_explanation = explain_connections("New PDF Research Uploaded", get_all_notes()[-len(files):])

    return (
        "\n".join(status_updates), 
        last_explanation, 
        format_all_notes_html(), 
        create_timeline_graph(G), 
        gr.update(choices=get_dropdown_choices())
    )

def remove_entry(selection):
    if not selection: 
        return "Select an ID", format_all_notes_html(), create_timeline_graph(G), gr.update()
    
    try:
        note_id = int(selection.split(":")[0])
        delete_note_by_id(note_id)
        rebuild_graph_from_db()
        return (
            f"🗑️ Deleted ID {note_id}", 
            format_all_notes_html(), 
            create_timeline_graph(G), 
            gr.update(choices=get_dropdown_choices(), value=None)
        )
    except Exception as e:
        return f"Error deleting: {str(e)}", format_all_notes_html(), create_timeline_graph(G), gr.update()

# --- UI Layout ---
# CSS and Theme moved to launch() to satisfy Gradio 6.0 requirements
with gr.Blocks() as app:
    gr.HTML("<h1>🧠 MindMap Live</h1><p style='opacity:0.6;'>PhD Research Portal | Candidate: Monisha Ravi Kumar</p>")

    with gr.Tabs():
        with gr.TabItem("📊 Dashboard"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 📜 Research Timeline")
                    timeline_html = gr.HTML(value=format_all_notes_html())
                    with gr.Group():
                        note_to_del = gr.Dropdown(label="Delete Entry", choices=get_dropdown_choices())
                        del_btn = gr.Button("🗑️ Remove", variant="stop")
                
                with gr.Column(scale=1):
                    gr.Markdown("### 🌐 Knowledge Graph")
                    graph_display = gr.Plot(value=create_timeline_graph(G))
                    explanation_box = gr.Textbox(
                        label="🔍 AI Connection Insight", 
                        interactive=False, 
                        lines=10, 
                        placeholder="Insights will appear after analysis..."
                    )

        with gr.TabItem("➕ Add Knowledge"):
            manual_input = gr.Textbox(label="Type a Note", lines=3, placeholder="Enter research notes or thoughts here...")
            file_input = gr.File(label="Upload PDFs", file_count="multiple", file_types=[".pdf"])
            submit_btn = gr.Button("Analyze & Sync", variant="primary")
            status_msg = gr.Markdown()

        with gr.TabItem("📧 Briefing"):
            email_target = gr.Textbox(label="Recipient Email", value="monisha21898@gmail.com")
            send_btn = gr.Button("Send Research Summary to Email")
            mail_status = gr.Markdown()

    # Event Listeners
    submit_btn.click(
        process_mixed_input, 
        inputs=[manual_input, file_input], 
        outputs=[status_msg, explanation_box, timeline_html, graph_display, note_to_del]
    )
    
    del_btn.click(
        remove_entry, 
        inputs=[note_to_del], 
        outputs=[status_msg, timeline_html, graph_display, note_to_del]
    )
    
    send_btn.click(
        lambda e: send_summary_email(generate_daily_summary(get_all_notes()), e), 
        inputs=[email_target], 
        outputs=[mail_status]
    )

if __name__ == "__main__":
    # Launch with fixed parameters for Gradio 6.0+
    app.launch(
        theme=gr.themes.Soft(), 
        css=".gradio-container {background-color:#0b0b14; color:white;}"
    )