import torch
import numpy as np
from torch.utils.data import Dataset
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

class EmotionDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings.reset_index(drop=True)
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx], dtype=torch.float32)
        return item

    def __len__(self):
        return len(self.encodings["input_ids"])

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average='weighted')
    acc = accuracy_score(labels, predictions)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

def predict_text(sentence, mlb, model, tokenizer):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    inputs = tokenizer(sentence, padding=True, truncation=True, return_tensors="pt")
    inputs = {key: value.to(device) for key, value in inputs.items()}
    outputs = model(**inputs)
    logits = outputs.logits
    logits = logits.cpu()
    probabilities = torch.sigmoid(logits).detach().numpy()

    # 예측 결과 정렬하고, 가장 높은 5개 추출
    sort_data = sorted(enumerate(probabilities[0]), key=lambda x: x[1], reverse=True)[:5]

    # 결과 출력
    for i, (index, intensity) in enumerate(sort_data, 1):
        emotion = mlb.classes_[index][0].lower()
        print(f"{i}번 감정: {emotion}, {i}번 감정 세기: {intensity:.2f}")