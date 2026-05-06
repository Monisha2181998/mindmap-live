import google.generativeai as genai


# Your working API Key
genai.configure(api_key="AIzaSyAYFu9RYjr5wnFfGgoJk2CJmiDfhtFAKBs")

def get_model_response(prompt):
    """
    Uses the exact model name verified in your AI Studio screenshot.
    """
    # These are the versions available to your specific account
    model_names = [
        'gemini-3-flash-preview', # From your screenshot
        'gemini-1.5-flash',
        'gemini-pro'
    ]
    
    for name in model_names:
        try:
            model = genai.GenerativeModel(name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            # If it's a 404, we try the next name in the list
            if "404" in str(e):
                continue
            return f"API Error: {str(e)}"
            
    return "Error: Could not find a compatible model. Please update your google-generativeai library."

def explain_connections(new_note_text, connections):
    if not connections:
        return "This is a unique thought with no direct overlaps found yet."

    context = "\n".join([
        f"- Linked to: '{c.content[:200]}...' via {getattr(c, 'shared_concepts', 'concepts')}" 
        for c in connections[:3]
    ])
    
    prompt = f"New note: {new_note_text}\nContext: {context}\nExplain the connection in 2 sentences."
    return get_model_response(prompt)

def generate_daily_summary(notes):
    if not notes:
        return "No research notes found to summarize."

    notes_text = "\n".join([f"- {n.content}" for n in notes])
    prompt = f"Summarize these research notes for a PhD portal:\n{notes_text}"
    return get_model_response(prompt)