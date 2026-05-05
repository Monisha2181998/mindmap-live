from huggingface_hub import InferenceClient

client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.3")

def explain_connections(new_note, connections):
    if not connections:
        return "This is a fresh idea — no connections to previous notes yet. Keep adding notes!"

    connection_text = ""
    for c in connections:
        connection_text += f"""
- Previous note: "{c['old_note']}"
  Written on: {c['timestamp']}
  Shared concepts: {', '.join(c['shared_concepts'])}
"""

    prompt = f"""You are a smart personal knowledge assistant.

A user just wrote this new note:
"{new_note}"

This note connects to their previous notes:
{connection_text}

In 2-3 sentences, explain in a friendly and insightful way:
1. How these notes connect
2. What this tells us about the user's thinking or learning journey

Be specific, mention the actual concepts. Do not use bullet points."""

    response = client.text_generation(prompt, max_new_tokens=200)
    return response

def generate_daily_summary(all_notes):
    if not all_notes:
        return "No notes yet. Start adding your thoughts!"

    notes_text = "\n".join([f"- {note.content}" for note in all_notes[-10:]])

    prompt = f"""You are a smart personal knowledge assistant.

Here are the user's recent notes:
{notes_text}

In 3-4 sentences, summarise:
1. The main topics they have been exploring
2. How these topics connect to each other
3. One insight about their learning journey

Be friendly, specific, and encouraging. Do not use bullet points."""

    response = client.text_generation(prompt, max_new_tokens=300)
    return response