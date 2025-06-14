from transformers import BertTokenizer, BertModel
import numpy as np;
import torch
from cleanText import cleanText

# Memuat tokenizer dan model Multilingual BERT
tokenizer = BertTokenizer.from_pretrained("indobenchmark/indobert-base-p2")
model = BertModel.from_pretrained("indobenchmark/indobert-base-p2")
# kw_model = KeyBERT('indobenchmark/indobert-base-p2')


# Detail Proses Dalam Menghasilkan Embediing
def get_embedding_verbose(text):
    if not text.strip():
        return {
            "text_clean": "",
            "tokens": [],
            "input_ids": [],
            "attention_mask": [],
            "embedding": np.zeros(model.config.hidden_size),
        }

    text_clean = cleanText(text)
    inputs = tokenizer(
        text_clean, return_tensors="pt", truncation=True, max_length=512, padding=True
    )

    tokens = tokenizer.tokenize(text_clean)
    input_ids = inputs["input_ids"].squeeze().tolist()
    attention_mask = inputs["attention_mask"].squeeze().tolist()

    with torch.no_grad():
        outputs = model(**inputs)

    # Mean-pooling dengan masking
    weights = inputs["attention_mask"].float()
    embeddings = outputs.last_hidden_state * weights.unsqueeze(-1)
    sentence_embedding = torch.sum(embeddings, dim=1).squeeze().numpy()

    return {
        "text_clean": text_clean,
        "tokens": tokens,
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "embedding": sentence_embedding,
    }
