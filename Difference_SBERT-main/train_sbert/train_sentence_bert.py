# 使用自己的数据集利用sbert训练文本相似度任务
from torch.utils.data import DataLoader
import torch.nn as nn
from sentence_transformers import SentenceTransformer, InputExample, losses
from sentence_transformers import models, evaluation
from preprocess import get_data
import os

os.environ["CUDA_VISIBLE_DEVICES"] = '0'
logpath = "train_logs"
name = "model_logs"

path = os.path.dirname(os.path.abspath(__file__))

model_path = path + "/text2vec-base-chinese"
word_embedding_model = models.Transformer(model_path, max_seq_length=256,)
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
dense_model = models.Dense(in_features=pooling_model.get_sentence_embedding_dimension(),
                           out_features=256, activation_function=nn.Tanh())
model = SentenceTransformer(modules=[word_embedding_model, pooling_model, dense_model])

x_train, x_test, y_train, y_test = get_data(r'train_data.csv')
train_examples = []
for s, label in zip(x_train, y_train):
    s1, s2 = s
    train_examples.append(
        InputExample(texts=[s1, s2], label=float(label))
    )
test_examples = []
for s, label in zip(x_test, y_test):
    s1, s2 = s
    test_examples.append(
        InputExample(texts=[s1, s2], label=float(label))
    )
train_loader = DataLoader(train_examples, shuffle=True, batch_size=8)
train_loss = losses.CosineSimilarityLoss(model)
model_save_path = path + '/resultModel2/'
evaluator = evaluation.EmbeddingSimilarityEvaluator.from_input_examples(test_examples)
model.fit(train_objectives=[(train_loader, train_loss)],
          epochs=50,
          evaluator=evaluator,
          warmup_steps=10,
          save_best_model=True,
          output_path=model_save_path,
          )

