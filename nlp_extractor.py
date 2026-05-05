import spacy

nlp = spacy.load("en_core_web_sm")

# Words to ignore
STOPWORDS_EXTRA = {"today", "meeting", "a meeting", "reading", "thing", "things"}

def extract_concepts(text):
    doc = nlp(text)
    concepts = []

    # Extract named entities
    for ent in doc.ents:
        concepts.append(ent.text.lower())

    # Extract noun chunks (captures "machine learning", "knowledge graphs" etc)
    for chunk in doc.noun_chunks:
        clean = chunk.text.lower().strip()
        # Skip if all stop words or in our ignore list
        if not all(token.is_stop for token in chunk) and clean not in STOPWORDS_EXTRA:
            # Remove leading articles like "a ", "the ", "an "
            for prefix in ["a ", "an ", "the "]:
                if clean.startswith(prefix):
                    clean = clean[len(prefix):]
            if len(clean) > 2:
                concepts.append(clean)

    # Extract important single nouns not already captured
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop:
            word = token.text.lower()
            if word not in " ".join(concepts) and word not in STOPWORDS_EXTRA:
                concepts.append(word)

    # Clean up and deduplicate
    concepts = [c.strip() for c in concepts if len(c.strip()) > 2]
    concepts = list(set(concepts))

    return concepts

# Test it
if __name__ == "__main__":
    test_notes = [
        "I studied machine learning and neural networks today",
        "Had a meeting about knowledge graphs and NLP research",
        "Applied for the ScaDS.AI PhD position at TU Dresden",
        "Reading about large language models and transformers",
        "Worked on Python code for deep learning project"
    ]

    for note in test_notes:
        concepts = extract_concepts(note)
        print(f"Note:     {note}")
        print(f"Concepts: {concepts}\n")