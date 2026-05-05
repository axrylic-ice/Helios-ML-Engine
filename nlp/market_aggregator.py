
import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util


device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)

anchors = [
    "Nigerian Naira devaluation and exchange rate increase",
    "FX market volatility and Naira depreciation vs USD",
    "Parallel market FX rates and currency pegging in Nigeria"
]

anchor_emb = model.encode(anchors, convert_to_tensor=True)
final_anchor = torch.mean(anchor_emb, dim=0)


def aggregate_market(events):

    if not events:
        return 0.5

    titles = [e["title"] for e in events]
    probs = np.array([e["probability"] for e in events])
    volumes = np.array([e.get("volume", 1) for e in events])

    # relevance scoring
    emb = model.encode(titles, convert_to_tensor=True)
    relevance = util.cos_sim(emb, final_anchor).cpu().numpy().flatten()

    weights = (relevance * np.log1p(volumes)) + 0.01

    if weights.sum() == 0:
        return float(probs.mean())

    return float((probs * weights).sum() / weights.sum())