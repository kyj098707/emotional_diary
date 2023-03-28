from sklearn.model_selection import train_test_split
from transformers import ElectraTokenizer, ElectraForSequenceClassification,  ElectraConfig
from transformers import TrainingArguments, Trainer

from sklearn.preprocessing import MultiLabelBinarizer

from prep_data import *
from function import *


# =================== VALUE ===================
DATA_PATH = "./before_csv"
TARGET_PATH = "./combine_csv"
EPOCHS = 1
BATCH_SIZE = 128
ChkPnt_DIR = "ChkPnt"
ChkLog_DIR = "ChnLog"
# =================== END VALUE ===================


# 다중분류에 따른 라벨 이진화
mlb = MultiLabelBinarizer()


# csv 데이터 병합 및 전처리
target_csv = combine_csv(DATA_PATH, TARGET_PATH)


# 병합 csv파일 읽어오기
df = pd.read_csv(target_csv)


# 라벨 튜플화
combine_label = [
    [(emotion, str(intensity)) for emotion, intensity in zip(row[3::2], row[4::2])] for _, row in df.iterrows()]


# =========== 튜플화 라벨 이진화 ============ #
encode_label = mlb.fit_transform(combine_label)

# ======== 모델 및 토크나이저 선언 =========== #
tokenizer = ElectraTokenizer.from_pretrained('monologg/koelectra-base-v3-discriminator')
config = ElectraConfig.from_pretrained("monologg/koelectra-base-v3-discriminator")
config.num_labels = len(mlb.classes_) # 다중분류에 따른 설정값 추가
model = ElectraForSequenceClassification.from_pretrained("monologg/koelectra-base-v3-discriminator", config=config)


# =============== 발화문 토큰화
text = df['발화문'].tolist()
encode_txt = tokenizer(text, padding=True, truncation=True, return_tensors="pt")
encode_df = pd.DataFrame({key: encode_txt[key].tolist() for key in encode_txt})


# =============== 데이터 분리
train_encodings, test_encodings, train_labels, test_labels = train_test_split(encode_df, encode_label, test_size=0.2, random_state=42)


# 라벨에 인코딩 데이터를 텐서로 매핑 -> 파이토치 데이터셋
train_dataset = EmotionDataset(train_encodings, train_labels)
test_dataset = EmotionDataset(test_encodings, test_labels)


# 모델 입력크기를 토큰 크기로 맞춘다.
model.resize_token_embeddings(len(tokenizer))


# arg 세팅 및 학습모델 선언
training_args = TrainingArguments(output_dir=ChkPnt_DIR,
                                  num_train_epochs=EPOCHS,
                                  per_device_train_batch_size=BATCH_SIZE,
                                  per_device_eval_batch_size=BATCH_SIZE,
                                  logging_dir=ChkLog_DIR
                                  )

trainer = Trainer(model=model,
                  args=training_args,
                  train_dataset=train_dataset,
                  eval_dataset=test_dataset,
                  compute_metrics=compute_metrics)


#학습
trainer.train()


test_text = '테스트용 문장'
predict_text(test_text, mlb, model, tokenizer)