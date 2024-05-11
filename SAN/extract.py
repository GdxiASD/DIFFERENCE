'''
Descripttion: 
version: 
Author: congsir
Date: 2022-09-07 09:13:13
LastEditors: Please set LastEditors
LastEditTime: 2022-09-22 10:43:38
'''
import hanlp
import re

# 句子
# sentence = ["他在浙江金华出生，他的名字叫金华。","2021年HanLPv2.1为生产环境带来次世代最先进的多语种NLP技术","阿婆主来到北京立方庭参观自然语义科技公司","我的希望是希望张晚霞的背影被晚霞映红"]
# sentence_list = ["刘小绪生于四川","美丽的刘小绪和帅气的李华写作业","刘小绪洗干净了衣服","这里有一个单纯的小朋友","这里有一个大人和一个小孩","建筑是主要的活动","贸易额为二百亿美元","    避雷器本体0.75倍直流参考电压下的漏电流应不大于100μA。"]
# sentence_list = ["应对3只试品的每1只试品施加3次操作电流冲击，其幅值分别约为避雷器操作配合电流的0.5倍、1倍和2倍。","操作冲击电流试验使用两种不同的配合电流波形，一个试验的电流波形为；视在波前时间30 μs，视在半峰值时间约为波前时间的两倍；另一个试验波形为：视在波前时间1 ms，视在半峰值时间约为波前时间的两倍。"]
# sentence_list = [    "避雷器快速波前保护水平取决于陡波冲击电流残压和波前冲击放电电压两者的最高值。","    应对3只试品的每1只试品施加4次陡波电流冲击，其幅值为避雷器陡波配合电流的0.1倍、0.5倍、1倍和2倍。所用电压测量系统的响应时间T和T1应不超过20 ns，电流测量回路响应时间应不超过150 ns，测量系统应符合GB/T 16927.2-1997的规定。残压按6.6确定。已确定的残压最大（或最小）值应画成残压与电流的曲线。在曲线上相应于配合电流读取的残压最大值，定义为避雷器陡波冲击保护水平。"]
# sentence_list = ["海洋由水组成"]
# 水,组成,海洋
# sentence_list =["刘小绪和李华写作业"]
# ['刘小绪和李华,写,作业']
# sentence_list = [" 棒形及盘形复合绝缘子伞裙、护套不应出现破损或龟裂、脱落、蚀损等现象，端头密封不应开裂、老化。"]
# ltp: 棒形, 复合, 绝缘子伞裙, 护套, 不应出现, 破损现象
# sentence_list = ["瓷质绝缘子伞裙不应破损，瓷质不应有裂纹，瓷釉不应烧损。"]
# ltp: 瓷质, 不应有, 裂纹
# ['瓷质,不应有,裂纹']
# sentence_list = ["线路运行维护单位对所管辖输电线路，均应按区段指定巡视责任人，同时明确其巡视的范围、周期及线路保护（包括宣传、组织群众护线）等责任。"]
# ltp: 单位,                          均应指定, 巡视责任人
# ['维护单位,指定同时明确,巡视责任人', '区段,指定同时明确,维护单位']
# ['维护单位,均应指定,巡视责任人', '区段,均应指定,维护单位']
# sentence_list = ["正常巡视包括对线路设备（本体、附属设备）及通道环境的检查，可以按全线或区段进行。巡视周期相对固定，并可动态调整。线路设备与通道环境的巡视可按不同的周期分别进行。"]
# ltp:空
# ['全线或区段,包括进行,正常巡视'], ['不同的周期,分别进行,通道设备与环境的巡视']
# ['全线或区段,可以进行,正常巡视'], ['不同的周期,可分别进行,通道设备与环境的巡视']
# sentence_list = ["    0.75倍直流参考电压下漏电流一般不超过50μA。多柱并联和额定电压216kV以上的避雷器漏电流由制造厂和用户协商规定。"]
# ltp:0.75倍直流, 参考, 电压下漏电流, 一般, 不超过, 50, 多柱, 并联, 协商规定
# ['参考电压下漏电流,一般不超过,50μA'], ['用户,协商规定,额定电压216kV以上的避雷器漏电流']
# ['参考电压下漏电流,一般不超过,50μA'], ['制造厂和用户,协商规定,多柱并联和额定电压216kV以上的避雷器漏电流']
# ['参考电压下漏电流,一般不超过,50μA'], ['制造厂和用户,规定,多柱并联和额定电压216kV以上的避雷器漏电流']
# sentence_list =["刘小绪和李华写作业"]
# ['刘小绪和李华,写,作业']
'''(暂时不用,直接输入句子影响后面存储)
name: 宁
brief: 输入句子，进行依存句法分析，返回依存句法列表字典
param  text 句子
return list_dic 词语依存句法列表字典
'''


def parser_sentence(sentence):
    # 依存句法
    dep_result = HanLP(sentence, tasks='dep')
    dep_result.pretty_print()
    list = []
    # 将依存句法结果拆分,分别用列表存储
    for value in dep_result.values():
        list.append(value)
    keys = list[0]
    values = list[1]

    # 用字典来存储依存句法结果（方便后面进行实体关系抽取）
    dic = dict([(k, []) for k in keys])
    # 字典中存储依存句法元组
    for i in range(len(keys)):
        if values[i][0] == 0:
            continue
        dic[keys[values[i][0] - 1]].append((values[i][1], keys[i]))
    print(dic)  # {'刘小绪': [], '生于': [('nsubj', '刘小绪'), ('dobj', '四川')], '四川': []}

    list_dic = []
    # 列表中存储依存句法字典
    for _, v in dic.items():
        dic_2 = dict([(m, n) for m, n in v])
        list_dic.append(dic_2)
    print(list_dic)  # [{}, {'nsubj': '刘小绪', 'dobj': '四川'}, {}]

    return list_dic


'''(暂时不用，字典中key值无法重复)
name: 宁
brief: 输入已经分词的列表，进行依存句法分析，返回依存句法列表字典
param  tok 分词列表
return list_dic_name 词语依存句法列表字典带中文名
        list_dic_id 词语依存句法列表字典带标号
'''


def parser_tok2(tok):
    # 依存句法
    dep_result = HanLP(tok, tasks='dep', skip_tasks='tok*')
    dep_result.pretty_print()
    list = []
    # 将依存句法结果拆分,分别用列表存储
    for value in dep_result.values():
        list.append(value)
    keys = list[1]
    values = list[0]
    # print(values) # [(2, 'top'), (0, 'root'), (5, 'assmod'), (3, 'assm'), (2, 'attr')]

    # 用字典来存储依存句法结果（方便后面进行实体关系抽取）
    dic_name = dict([(k, []) for k in keys])
    dic_id = dict([(k, []) for k in keys])
    print(dic_id)
    # 字典中存储依存句法元组
    for i in range(len(keys)):
        # 跳过root关系
        if values[i][0] == 0:
            continue
        # 合并关系，将top替换为nsubj
        if values[i][1] == 'top':
            values[i] = (values[i][0], 'nsubj')

        dic_name[keys[values[i][0] - 1]].append((values[i][1], keys[i]))
        dic_id[keys[values[i][0] - 1]].append((values[i][1], i))
    # print(dic_name) # {'刘小绪': [], '生于': [('nsubj', '刘小绪'), ('dobj', '四川')], '四川': []}
    # print(dic_id) # {'刘小绪': [], '生于': [('nsubj', 0), ('dobj', 2)], '四川': []}
    list_dic_name = []
    list_dic_id = []
    # 列表中存储依存句法字典
    for _, v in dic_name.items():
        dic_2 = dict([(m, n) for m, n in v])
        list_dic_name.append(dic_2)
    for _, v in dic_id.items():
        dic_2 = dict([(m, n) for m, n in v])
        list_dic_id.append(dic_2)
    print(list_dic_name)  # [{}, {'nsubj': '刘小绪', 'dobj': '四川'}, {}]
    print(list_dic_id)  # [{}, {'nsubj': 0, 'dobj': 2}, {}]

    return list_dic_name, list_dic_id


'''
name: 宁
brief: 输入已经分词的列表，进行依存句法分析，返回依存句法列表字典
param  tok 分词列表
return list_dic_id 词语依存句法列表字典带标号
        
'''


def parser_tok(tok):
    # 依存句法
    dep_result = HanLP(tok, tasks='dep', skip_tasks='tok*')
    dep_result2 = HanLP(tok, tasks=['dep', 'pos/pku'], skip_tasks='tok*')
    # dep_result2.pretty_print()
    list = []
    # 将依存句法结果拆分,分别用列表存储
    for value in dep_result.values():
        list.append(value)
    keys = list[1]

    values = list[0]

    # 存储元组列表
    list_tuple_id = []
    # 定义有长度的空列表
    for i in range(len(keys)):
        list_tuple_id.append([])

    # 向列表中加入关系
    for i in range(len(keys)):
        # 关系位置
        loc = values[i][0]
        # 关系类型
        relation = values[i][1]
        # 跳过root
        if relation == "root":
            continue

        # 合并关系，将top替换为nsubj
        if relation == 'top':
            relation = 'nsubj'

        list_tuple_id[values[i][0] - 1].append((relation, i))

    # 存储字典列表
    list_dic_id = []
    # 将列表转换为字典列表
    for i in range(len(keys)):
        list_dic_id.append(dict([(m, n) for m, n in list_tuple_id[i]]))

    # print(list_dic_id)
    return list_dic_id


'''（暂时废弃）
name: 
brief: 
param {*} tok
param {*} list_dic_id
param {*} i
return {*}
'''


def extract2(tok, list_dic_id, i):
    # 当前词的词典
    dic = list_dic_id[i]
    # 存放结果
    result = []
    # 主谓宾关系：刘小绪生于四川
    if 'nsubj' in dic.keys() and 'dobj' in dic.keys():
        # 头实体：主谓关系的主语
        entity1 = tok[dic['nsubj']]

        # 并列关系1
        # 刘小绪和李华写作业
        # dic['nsubj'] 即主语在依存字典中的索引
        if 'conj' in list_dic_id[dic['nsubj']]:
            # 判断主语前是否有修饰词
            if 'nummod' in list_dic_id[dic['nsubj']]:
                decoration = tok[list_dic_id[dic['nsubj']]['nummod']]
                entity1 = decoration + entity1
            # 头实体2：主谓关系中主语的并列词
            entity1_conj = tok[list_dic_id[dic['nsubj']]['conj']]
            # 关系：当前词
            relation = tok[i]
            # 尾实体：动宾关系的宾语
            entity2 = tok[dic['dobj']]
            # 判断宾语前是否有修饰词
            if 'nummod' in list_dic_id[dic['dobj']]:
                decoration = tok[list_dic_id[dic['dobj']]['nummod']]
                entity2 = decoration + entity2
            result.append(entity1 + "," + relation + "," + entity2)
            result.append(entity1_conj + "," + relation + "," + entity2)
        # 并列关系2
        # 这里有一个大人和一个小孩
        elif 'conj' in list_dic_id[dic['dobj']]:
            # 判断主语前是否有修饰词
            if 'nummod' in list_dic_id[dic['nsubj']]:
                decoration = tok[list_dic_id[dic['nsubj']]['nummod']]
                entity1 = decoration + entity1
            # 头实体2：主题词的并列词
            entity2_conj = tok[list_dic_id[dic['dobj']]['conj']]
            if 'nummod' in list_dic_id[list_dic_id[dic['dobj']]['conj']]:
                decoration = tok[list_dic_id[list_dic_id[dic['dobj']]['conj']]['nummod']]
                entity2_conj = decoration + entity2_conj
            # 关系：当前词
            relation = tok[i]
            # 尾实体：动宾关系的宾语
            entity2 = tok[dic['dobj']]
            # 判断宾语前是否有修饰词
            if 'nummod' in list_dic_id[dic['dobj']]:
                decoration = tok[list_dic_id[dic['dobj']]['nummod']]
                entity2 = decoration + entity2
            result.append(entity1 + "," + relation + "," + entity2_conj)
            result.append(entity1 + "," + relation + "," + entity2)
        else:
            # 判断主语前是否有修饰词
            if 'nummod' in list_dic_id[dic['nsubj']]:
                decoration = tok[list_dic_id[dic['nsubj']]['nummod']]
                entity1 = decoration + entity1
            # 尾实体：动宾关系的宾语
            entity2 = tok[dic['dobj']]
            # 判断宾语前是否有修饰词
            if 'nummod' in list_dic_id[dic['dobj']]:
                decoration = tok[list_dic_id[dic['dobj']]['nummod']]
                entity2 = decoration + entity2
            # 关系：当前词（即同时含有主谓关系和动宾关系的词）
            relation = tok[i]
            result.append(entity1 + "," + relation + "," + entity2)

    # 动补结构：刘小绪洗干净了衣服
    if 'rcomp' in dic.keys() and 'nsubj' in dic.keys() and 'dobj' in dic.keys():
        # 头实体：主谓关系的主语
        entity1 = tok[dic['nsubj']]
        # 动补关系中的补语
        complement = tok[dic['rcomp']]
        # 尾实体：动宾关系的宾语
        entity2 = tok[dic['dobj']]
        # 是否有附加关系
        if 'asp' in dic.keys():
            # 时态标记
            subjion = tok[dic['asp']]
            # 关系：当前词+补语+加时态标记
            relation = tok[i] + complement + subjion
            result.append(entity1 + "," + relation + "," + entity2)
        else:
            # 关系：当前词+补语
            relation = tok[i] + complement
            result.append(entity1 + "," + relation + "," + entity2)

    # 属性关系：贸易额为二百亿美元
    if 'nsubj' in dic.keys() and 'attr' in dic.keys():
        # 头实体：主谓关系的主语
        entity1 = tok[dic['nsubj']]

        if bool(list_dic_id[dic['attr']]):
            pass
            # print(12345)
        # 修饰关系：二百亿美元
        if 'assmod' in list_dic_id[dic['attr']]:
            # 关系：当前词
            relation = tok[i]
            # 尾实体：属性词
            entity2 = tok[dic['attr']]
            # 修饰关系：修饰属性词的词语
            decoration = tok[list_dic_id[dic['attr']]['assmod']]
            # 拼接
            entity2 = decoration + entity2
            result.append(entity1 + "," + relation + "," + entity2)
        elif 'nummod' in list_dic_id[dic['attr']]:
            # 关系：当前词
            relation = tok[i]
            # 尾实体：属性词
            entity2 = tok[dic['attr']]
            # 修饰关系：修饰属性词的词语
            decoration = tok[list_dic_id[dic['attr']]['nummod']]
            # 拼接
            entity2 = decoration + entity2
            result.append(entity1 + "," + relation + "," + entity2)
        else:
            # 关系：当前词
            relation = tok[i]
            # 尾实体：属性词
            entity2 = tok[dic['attr']]
            result.append(entity1 + "," + relation + "," + entity2)

    # 定中结构
    # if 'amod' in dic.keys():

    # 状动结构：父亲非常喜欢跑步
    # 非常 是 跑步的状语，关系应该为非常喜欢

    # 状动补结构：

    # 定语后置：父亲是来自肯尼亚的留学生

    # 介宾关系：刘小绪就职于学校
    # 于 和 学校 是介宾关系

    # 宾语前置结构：海洋由水组成
    return result


def extract(tok, pos, list_dic_id, i):
    # 当前词的词典
    dic = list_dic_id[i]
    # 存放结果
    result = []
    if pos[i] == 'v':
        # 主谓宾关系：刘小绪生于四川
        if 'nsubj' in dic.keys() and 'dobj' in dic.keys():
            # 头实体：主谓关系的主语
            entity1 = complete_e(tok, pos, list_dic_id, dic['nsubj'])

            # 尾实体：动宾关系的宾语
            entity2 = complete_e(tok, pos, list_dic_id, dic['dobj'])
            # 关系：当前词（即同时含有主谓关系和动宾关系的词）
            # relation = tok[i]
            relation = complete_r(tok, pos, list_dic_id, i)
            result.append(entity1 + "," + relation + "," + entity2)
        # # 主谓宾关系：刘小绪生于四川
        # if 'nsubj' in dic.keys() and 'dobj' in dic.keys():
        #     # 头实体：主谓关系的主语
        #     entity1 = complete_e(tok,pos, list_dic_id, dic['nsubj'])

        #     # 并列关系1
        #     # 刘小绪和李华写作业
        #     # dic['nsubj'] 即主语在依存字典中的索引
        #     if 'conj' in list_dic_id[dic['nsubj']]:
        #         # 头实体2：主谓关系中主语的并列词
        #         entity1_conj = complete_e(tok, pos,list_dic_id, list_dic_id[dic['nsubj']]['conj'])
        #         # 关系：当前词
        #         # relation = tok[i]
        #         relation = complete_r(tok, pos,list_dic_id, i)
        #         # 尾实体：动宾关系的宾语
        #         entity2 = complete_e(tok,pos, list_dic_id, dic['dobj'])

        #         result.append(entity1 + "," + relation + "," + entity2)
        #         result.append(entity1_conj + "," + relation + "," + entity2)
        #     # 并列关系2
        #     # 这里有一个大人和一个小孩
        #     elif 'conj' in list_dic_id[dic['dobj']]:

        #         # 头实体2：主题词的并列词
        #         entity2_conj = complete_e(tok, pos,list_dic_id, list_dic_id[dic['dobj']]['conj'])
        #         # 关系：当前词
        #         # relation = tok[i]
        #         relation = complete_r(tok, pos,list_dic_id, i)
        #         # 尾实体：动宾关系的宾语
        #         entity2 = complete_e(tok,pos, list_dic_id, dic['dobj'])
        #         result.append(entity1 + "," + relation + "," + entity2_conj)
        #         result.append(entity1 + "," + relation + "," + entity2)
        #     else:

        #         # 尾实体：动宾关系的宾语
        #         entity2 = complete_e(tok,pos, list_dic_id, dic['dobj'])
        #         # 关系：当前词（即同时含有主谓关系和动宾关系的词）
        #         # relation = tok[i]
        #         relation = complete_r(tok, pos,list_dic_id, i)
        #         result.append(entity1 + "," + relation + "," + entity2)

        # 属性关系：贸易额为二百亿美元
        if 'nsubj' in dic.keys() and 'attr' in dic.keys():
            # 头实体：主谓关系的主语
            entity1 = complete_e(tok, pos, list_dic_id, dic['nsubj'])
            # 关系：当前词
            # relation = tok[i]
            relation = complete_r(tok, pos, list_dic_id, i)
            # 尾实体：属性词
            entity2 = complete_e(tok, pos, list_dic_id, dic['attr'])
            result.append(entity1 + "," + relation + "," + entity2)

        # 比较词
        if 'nsubj' in dic.keys() and 'range' in dic.keys():
            # 头实体：主谓关系的主语
            entity1 = complete_e(tok, pos, list_dic_id, dic['nsubj'])
            # 关系：当前词
            # relation = tok[i]
            relation = complete_r(tok, pos, list_dic_id, i)
            # 尾实体
            entity2 = complete_e(tok, pos, list_dic_id, dic['range'])
            result.append(entity1 + "," + relation + "," + entity2)
        # 宾语前置结构：海洋由水组成
        if 'nsubj' in dic.keys() and 'prep' in dic.keys():
            if 'pobj' in list_dic_id[dic['prep']]:
                if list_dic_id[dic['prep']]['pobj'] < i:
                    # 头实体
                    entity1 = complete_e(tok, pos, list_dic_id, list_dic_id[dic['prep']]['pobj'])
                    # 尾实体
                    entity2 = complete_e(tok, pos, list_dic_id, dic['nsubj'])
                    # 关系
                    relation = complete_r(tok, pos, list_dic_id, i)
                    result.append(entity1 + "," + relation + "," + entity2)

    return result


def complete_r(tok, pos, list_dic_id, word_index):
    # 当前词的词典
    dic = list_dic_id[word_index]
    # 前置修饰
    prefix = ''
    # 后置修饰
    postfix = ''
    for key, value in dic.items():
        # 数词修饰词
        if key == 'nummod':
            if word_index > value:
                prefix += complete_r(tok, pos, list_dic_id, value)
            else:
                postfix += complete_r(tok, pos, list_dic_id, value)
        # 关系修饰词
        if key == 'assmod':
            if word_index > value:
                prefix += complete_r(tok, pos, list_dic_id, value)
            else:
                postfix += complete_r(tok, pos, list_dic_id, value)
        # 关系修饰词
        if key == 'lobj':
            if word_index > value:
                prefix += complete_r(tok, pos, list_dic_id, value)
            else:
                postfix += complete_r(tok, pos, list_dic_id, value)
        # 名词修饰
        if key == 'nn':
            if word_index > value:
                prefix += complete_r(tok, pos, list_dic_id, value)
            else:
                postfix += complete_r(tok, pos, list_dic_id, value)
        # 定语修饰
        if key == 'rcmod':
            if word_index > value:
                prefix += complete_r(tok, pos, list_dic_id, value)
            else:
                postfix += complete_r(tok, pos, list_dic_id, value)
        # 依赖关系dep
        # if key == 'dep':
        #     if word_index > value:
        #         prefix += complete_r(tok,pos, list_dic_id, value)
        #     else:
        #         postfix += complete_r(tok,pos, list_dic_id, value)
        # 类别修饰
        if key == 'clf':
            if word_index > value:
                prefix += complete_r(tok, pos, list_dic_id, value)
            else:
                postfix += complete_r(tok, pos, list_dic_id, value)
        # 形容词修饰 amod
        if key == 'amod':
            if word_index > value:
                prefix += complete_r(tok, pos, list_dic_id, value)
            else:
                postfix += complete_r(tok, pos, list_dic_id, value)

        # '的'
        if key == 'assm' or key == 'cpm':
            if word_index > value:
                prefix += complete_r(tok, pos, list_dic_id, value)
            else:
                postfix += complete_r(tok, pos, list_dic_id, value)
        # 限定语
        if key == 'det':
            if word_index > value:
                prefix += complete_r(tok, pos, list_dic_id, value)
            else:
                postfix += complete_r(tok, pos, list_dic_id, value)
        # 修饰词advmod：最
        if key == 'advmod':
            if word_index > value:
                prefix += complete_r(tok, pos, list_dic_id, value)
            else:
                postfix += complete_r(tok, pos, list_dic_id, value)
        # 状语
        if key == 'rcomp':
            if word_index > value:
                prefix += complete_r(tok, pos, list_dic_id, value)
            else:
                postfix += complete_r(tok, pos, list_dic_id, value)
        # 否定词
        if key == 'neg':
            if word_index > value:
                prefix += complete_r(tok, pos, list_dic_id, value)
            else:
                postfix += complete_r(tok, pos, list_dic_id, value)
        # '了'
        if key == 'asp':
            if word_index > value:
                prefix += complete_r(tok, pos, list_dic_id, value)
            else:
                postfix += complete_r(tok, pos, list_dic_id, value)
        # 修饰词
        if key == 'mmod':
            if word_index > value:
                prefix += complete_r(tok, pos, list_dic_id, value)
            else:
                postfix += complete_r(tok, pos, list_dic_id, value)
        # # 并列连接词：‘和’
        # if key == 'cc':
        #     if word_index > value:
        #         prefix += complete_r(tok,pos, list_dic_id, value)
        #     else:
        #         postfix += complete_r(tok,pos, list_dic_id, value)
        # # 并列词
        # if key == 'conj':
        #     if word_index > value:
        #         prefix += complete_r(tok,pos, list_dic_id, value)
        #     else:
        #         postfix += complete_r(tok,pos, list_dic_id, value)
    return prefix + tok[word_index] + postfix


def complete_e(tok, pos, list_dic_id, word_index):
    # 当前词的词典
    dic = list_dic_id[word_index]
    # 前置修饰
    prefix = ''
    # 后置修饰
    postfix = ''
    for key, value in dic.items():
        # 数词修饰词
        if key == 'nummod':
            if word_index > value:
                prefix += complete_e(tok, pos, list_dic_id, value)
            else:
                postfix += complete_e(tok, pos, list_dic_id, value)
        # 关系修饰词
        if key == 'assmod':
            if word_index > value:
                prefix += complete_e(tok, pos, list_dic_id, value)
            else:
                postfix += complete_e(tok, pos, list_dic_id, value)
        # 关系修饰词
        if key == 'lobj':
            if word_index > value:
                prefix += complete_e(tok, pos, list_dic_id, value)
            else:
                postfix += complete_e(tok, pos, list_dic_id, value)
        # 动词修饰vmod
        if key == 'vmod':
            if word_index > value:
                prefix += complete_e(tok, pos, list_dic_id, value)
            else:
                postfix += complete_e(tok, pos, list_dic_id, value)
        # 名词修饰
        if key == 'nn':
            if word_index > value:
                prefix += complete_e(tok, pos, list_dic_id, value)
            else:
                postfix += complete_e(tok, pos, list_dic_id, value)
        # 定语修饰
        if key == 'rcmod':
            if word_index > value:
                prefix += complete_e(tok, pos, list_dic_id, value)
            else:
                postfix += complete_e(tok, pos, list_dic_id, value)
        # # 介宾
        # if key == 'pobj':
        #     if word_index > value:
        #         prefix += complete_e(tok,pos, list_dic_id, value)
        #     else:
        #         postfix += complete_e(tok,pos, list_dic_id, value)
        # 依赖关系dep
        if key == 'dep':
            if word_index > value:
                prefix += complete_e(tok, pos, list_dic_id, value)
            else:
                postfix += complete_e(tok, pos, list_dic_id, value)
        # 类别修饰
        if key == 'clf':
            if word_index > value:
                prefix += complete_e(tok, pos, list_dic_id, value)
            else:
                postfix += complete_e(tok, pos, list_dic_id, value)
        # 形容词修饰 amod
        if key == 'amod':
            if word_index > value:
                prefix += complete_e(tok, pos, list_dic_id, value)
            else:
                postfix += complete_e(tok, pos, list_dic_id, value)

        # '的'
        if key == 'assm' or key == 'cpm':
            if word_index > value:
                prefix += complete_e(tok, pos, list_dic_id, value)
            else:
                postfix += complete_e(tok, pos, list_dic_id, value)
        # 限定语
        if key == 'det':
            if word_index > value:
                prefix += complete_e(tok, pos, list_dic_id, value)
            else:
                postfix += complete_e(tok, pos, list_dic_id, value)
        # 修饰词advmod：最
        if key == 'advmod':
            if word_index > value:
                prefix += complete_e(tok, pos, list_dic_id, value)
            else:
                postfix += complete_e(tok, pos, list_dic_id, value)
        # 并列连词
        if key == 'cc':
            if word_index > value:
                prefix += complete_e(tok, pos, list_dic_id, value)
            else:
                postfix += complete_e(tok, pos, list_dic_id, value)
        # 并列词
        if key == 'conj':
            if word_index > value:
                prefix += complete_e(tok, pos, list_dic_id, value)
            else:
                postfix += complete_e(tok, pos, list_dic_id, value)
        # 名词
        # if key == 'nn':
        #     if word_index > value:
        #         prefix += complete_e(tok,pos, list_dic_id, value)
        #     else:
        #         postfix += complete_e(tok,pos, list_dic_id, value)
        if pos == 'v':
            # 状语
            if key == 'rcomp':
                if word_index > value:
                    prefix += complete_e(tok, pos, list_dic_id, value)
                else:
                    postfix += complete_e(tok, pos, list_dic_id, value)
            # 否定词
            if key == 'neg':
                if word_index > value:
                    prefix += complete_e(tok, pos, list_dic_id, value)
                else:
                    postfix += complete_e(tok, pos, list_dic_id, value)
            # '了'
            if key == 'asp':
                if word_index > value:
                    prefix += complete_e(tok, pos, list_dic_id, value)
                else:
                    postfix += complete_e(tok, pos, list_dic_id, value)
            # 名词性修饰（有待考虑）
            if key == 'nsubj':
                if word_index > value:
                    prefix += complete_e(tok, pos, list_dic_id, value)
                else:
                    postfix += complete_e(tok, pos, list_dic_id, value)
        # if key == ''
        # # 数词修饰词
        # if dic.__contains__('nummod'):

        #     for key,value in dic.items():
        #         # print(key,value)

        #         if dic.__contains__('cc'):
        #             if key != 'nummod':
        #                 break
        #         prefix += complete(tok, list_dic_id, value)
        # # 关系修饰词
        # if dic.__contains__('assmod'):
        #     for key,value in dic.items():
        #         prefix += complete(tok, list_dic_id, value)
        #     pass
        # # 的
        # if dic.__contains__('assm'):
        #     for key,value in dic.items():
        #         prefix += complete(tok, list_dic_id, value)

        # # 补充主语
        # if dic.__contains__('nsubj'):

        #     pass
        # # 补充宾语
        # if dic.__contains__('dobj'):
        #     pass

    return prefix + tok[word_index] + postfix


def pretreatment(sentence):
    # 处理小标题,例如1 
    # sentence = re.sub(r'[0-9] ',"",sentence)

    # 处理标题等级，例如：7.3.7
    sentence = re.sub(r'[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*', "", sentence)
    # 处理标题等级，例如：B.1.2
    sentence = re.sub(r'[A-Z]\.[0-9][0-9]*\.[0-9][0-9]*', "", sentence)
    # 处理标题等级，例如：7.3.7.3
    sentence = re.sub(r'[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*', "", sentence)
    # 处理标题等级，例如：7.3.7.3.2
    sentence = re.sub(r'[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*', "", sentence)

    # 处理特殊字符串，例如&nbsp
    sentence = sentence.replace("&nbsp", "")
    # 处理小标题,例如2）
    sentence = re.sub(r' [0-9]\)', "", sentence)
    sentence = re.sub(r' [0-9]）', "", sentence)

    # 处理小标题,例如b）
    sentence = re.sub(r' [a-z]\)', "", sentence)
    sentence = re.sub(r' [a-z]）', "", sentence)

    # 处理小标题,例如〈3〉：
    sentence = re.sub(r'〈[0-9][0-9]*〉：', "", sentence)
    # 处理小标题,例如〈3〉
    sentence = re.sub(r'〈[0-9][0-9]*〉', "", sentence)

    # 处理附录
    sentence = re.sub(r'附录[A-Z]', "", sentence)
    # 处理html语句
    sentence = re.sub(r'<\w+?>', "", sentence)
    sentence = re.sub(r'</\w+?>', "", sentence)
    sentence = re.sub(r'<p .*?>', "", sentence)
    sentence = re.sub(r'<a .*?>', "", sentence)
    # 处理空白字符
    sentence = re.sub(r'\s', "", sentence)
    # 处理多个分号的情况
    sentence = sentence.replace(";;", "")

    return sentence


from preprocess import get_data

HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)


def extract_to_tri(data):
    tok_pos = HanLP(pretreatment(data), tasks=['dep', 'tok/coarse'])
    # 分词结果
    tok = tok_pos['tok/coarse']
    dep_result = HanLP(tok, tasks=['dep', 'pos/pku'], skip_tasks='tok*')
    # 词性标注结果
    pos = dep_result['pos/pku']
    # 依存句法分析
    list_dic_id = parser_tok(tok)
    # 存放三元组结果
    triple_list = []
    # 遍历依存句法结果，提取实体关系
    for i in range(len(tok)):
        triple_i = extract(tok, pos, list_dic_id, i)
        if len(triple_i) != 0:
            triple_list.append(triple_i)

    # print(triple_list)
    triple_list = str(triple_list).replace("'", '')
    triple_list = triple_list.replace("[", '')
    triple = triple_list.replace("]", '')
    return triple


if __name__ == '__main__':
    s = [
        "变压器、电抗器在装卸和运输过程不应有严重冲击和振动。电压在220kV及以上且容量在150MVA 及以上的变压器和电压在330kV及以上的电抗器均应装设三维冲撞记录仪。冲击记录纸应符合制造厂及合同规定。",
        "110（66）kV 及以上电压等级变压器在运输过程中，应按照相应规范安装具有时标且有合适量程的三维冲击记录仪。变压器就位后，制造厂、运输部门、监理单位、用户四方人员应共同验收，记录纸和押运记录应提供给用户留存。",
        "HG/T 2887-2018《变压器类产品用橡胶密封制品》中3.2 制品的尺寸公差 3.2.2： O形圈尺寸和公差应符合GB/T 3452.1-2005中G系列的要求；3.2.3：除 O形圈以外的其他模压制品、压出制品、压延胶板的尺寸公差应分别符合GB/T 3672.1-2002中M3级、E2级、ST3级的要求。3.3制品的外观质量3.3.1采用目 视检测；3.3.2： O形圈应符合GB/T 3452.2中S级的要求；非O形圈模压制品、 压出制品、压延胶板的外观质量应符合HG/T3090的规定。",]
    for i in s:
        g1 = extract_to_tri(i)
        print(g1)
