# -*- coding: utf-8 -*-



import os
import sys
import torch
pwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(pwd)


class Hyperparameters:
    """ 参数设置 """
    
    # 基本参数
    EPOCHS = 10
    SAMPLES = 10000 
    BATCH_SIZE = 8
    LR = 1e-5
    DROPOUT = 0.1 
    MAXLEN = 256
    POOLING = 'cls'   # choose in ['cls', 'pooler', 'first-last-avg', 'last-avg']
    # DEVICE = torch.device('cpu') # torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # 预训练模型目录
    BERT = 'pretrained_model/bert_pytorch'
    BERT_WWM_EXT = 'pretrained_model/bert_wwm_ext_pytorch'
    # ROBERTA = 'F:/celery/simcse_pytorch/roberta_pytorch'
    ROBERTA = r'D:\Codes\finetune_sbert\BERT2\my-bert-model'
    pretrained_model_path = ROBERTA 
    
    # 微调后参数存放位置
    SAVE_PATH_UNSUP = os.path.join(pwd, 'model', 'saved_model', 'simcse_unsup.pt')
    LOAD_PATH_UNSUP = os.path.join(pwd, 'model', 'load_model', 'simcse_unsup.pt')
    SAVE_PATH_SUP = os.path.join(pwd, 'model', 'saved_model', 'simcse_sup.pt')
    LOAD_PATH_SUP = os.path.join(pwd, 'model', 'load_model', 'simcse_sup.pt')
 

if __name__ == '__main__': 
    #
    hp = Hyperparameters()
    print(hp.pretrained_model_path)
    
