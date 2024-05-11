import numpy as np
from sklearn.metrics import classification_report
from sentence_transformers import SentenceTransformer, util
from preprocess import get_data
import os
import matplotlib.pyplot as plt

model_path = r'/resultModel'
model = SentenceTransformer(model_path)

x_train, x_test, y_train, y_test = get_data(r'train_data.csv')
s1 = np.array(x_test)[:, 0]
s2 = np.array(x_test)[:, 1]
embedding1 = model.encode(s1, convert_to_tensor=True)
embedding2 = model.encode(s2, convert_to_tensor=True)
print(path)
thresholds = [i for i in np.linspace(0, 0.99, 100)]
precision_scores = []
recall_scores = []
f1_scores = []
print('threshold is following as ', thresholds)
for threshold in thresholds:
    for i in range(len(s1)):
        similarity = util.cos_sim(embedding1[i], embedding2[i])
        if similarity > threshold:
            pre_labels[i] = 1
    report = classification_report(y_test, pre_labels, output_dict=True, zero_division=1)
    precision_scores.append(report['weighted avg']['precision'])
    recall_scores.append(report['weighted avg']['recall'])
    f1_scores.append(report['weighted avg']['f1-score'])
plt.plot(thresholds, precision_scores, label='Precision')
plt.plot(thresholds, recall_scores, label='Recall')
plt.plot(thresholds, f1_scores, label='F1 Score')
plt.xlabel('Threshold')
plt.ylabel('Score')
plt.title('Evaluation Metrics vs. Threshold')
plt.legend()
plt.savefig('Score.png')
