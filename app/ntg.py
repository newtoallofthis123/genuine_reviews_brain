from transformers import AutoTokenizer, AutoModelForSequenceClassification  # type: ignore
import torch


def predict_review(reviews):
    tokenizer = AutoTokenizer.from_pretrained(
        "zayuki/computer_generated_fake_review_detection")
    model = AutoModelForSequenceClassification.from_pretrained(
        "zayuki/computer_generated_fake_review_detection", from_tf=True)

    inputs = tokenizer(reviews, return_tensors="pt",
                       padding=True, truncation=True, max_length=512)

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    predicted_classes = torch.argmax(probabilities, dim=-1)

    res = []

    for i, text in enumerate(input_texts):
        if predicted_classes[i].item() == 1:
            res.append(True)
        else:
            res.append(False)

    return res
