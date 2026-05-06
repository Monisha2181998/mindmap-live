import spacy

nlp = spacy.load("en_core_web_sm")

def extract_concepts(text):
    doc = nlp(text)
    concepts = []

    # 1. Segregate Named Entities (ScaDS.AI researchers value this for Big Data)
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "GPE", "ORG", "PRODUCT"]:
            concepts.append(ent.text.lower())

    # 2. Segregate Noun Chunks (Technical terms)
    for chunk in doc.noun_chunks:
        clean = chunk.text.lower().strip()
        # Remove common filler words
        for prefix in ["a ", "an ", "the "]:
            if clean.startswith(prefix): clean = clean[len(prefix):]
        if len(clean) > 2:
            concepts.append(clean)

    # Remove duplicates and return[cite: 8]
    return list(set(concepts))