

# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# import torch

# # Load model once (do it in a global or init block)
# MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# def analyze_sentiment(text):
#     inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
#     outputs = model(**inputs)
#     probs = torch.nn.functional.softmax(outputs.logits, dim=1)
#     sentiment_score = probs[0][1].item() - probs[0][0].item()  # positive - negative

#     if sentiment_score > 0.2:
#         label = "positive"
#     elif sentiment_score < -0.2:
#         label = "negative"
#     else:
#         label = "neutral"

#     return label, sentiment_score
