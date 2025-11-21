# vector_memory.py - embedding-backed memory with TF-IDF fallback
import os, json
from pathlib import Path
import numpy as np

USE_OPENAI_EMBEDDINGS = os.environ.get('USE_OPENAI_EMBEDDINGS', 'false').lower() == 'true'

class VectorMemory:
    def __init__(self, path='memory/vector_store.json'):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text(json.dumps({'documents': []}))
        self._load()

    def _load(self):
        self.store = json.loads(self.path.read_text())
        self.documents = self.store.get('documents', [])

    def _save(self):
        self.store['documents'] = self.documents
        self.path.write_text(json.dumps(self.store, indent=2))

    def _get_embedding(self, text):
        if USE_OPENAI_EMBEDDINGS:
            try:
                import openai
                api_key = os.environ.get('OPENAI_API_KEY')
                openai.api_key = api_key
                resp = openai.Embedding.create(model='text-embedding-3-small', input=text)
                vec = resp['data'][0]['embedding']
                return vec
            except Exception as e:
                print('Embedding error, using fallback:', e)
        # Fallback: simple hash-based pseudo-embedding for offline mode
        arr = np.zeros(128, dtype=float)
        for i, ch in enumerate(text[:128]):
            arr[i % 128] += (ord(ch) % 31) / 31.0
        return arr.tolist()

    def add_document(self, doc_id, text, metadata=None):
        vec = self._get_embedding(text)
        self.documents.append({'id': doc_id, 'text': text, 'embedding': vec, 'metadata': metadata or {}})
        self._save()

    def query(self, text, top_k=5):
        qv = self._get_embedding(text)
        # compute cosine similarity
        import math
        sims = []
        for d in self.documents:
            v = d['embedding']
            # ensure same length
            m = min(len(v), len(qv))
            dot = sum(v[i]*qv[i] for i in range(m))
            nv = math.sqrt(sum((vi*vi) for vi in v[:m]))
            nq = math.sqrt(sum((qi*qi) for qi in qv[:m]))
            score = dot / (nv*nq+1e-9)
            sims.append((score, d))
        sims.sort(key=lambda x: x[0], reverse=True)
        return [d for s,d in sims[:top_k]]
