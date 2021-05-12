# -*- coding: utf-8 -*-
import jieba
from gensim import corpora, models
from gensim.similarities import Similarity


class getrequirement:
    def __init__(self, funData, nfunData):
        # 功能需求
        self.funData = funData
        # 非功能需求
        self.nfunData = nfunData

    @property
    def GetRelatedFR_NFR(self):
        Result = []
        corpora_documents = []
        # item_text 一个分析的文本
        for item_text in self.funData:
            item_str = jieba.lcut(item_text)
            corpora_documents.append(item_str)
        dictionary = corpora.Dictionary(corpora_documents)
        #  通过下面一句得到语料中每一篇文档对应的稀疏向量（这里是bow向量）stopwords
        corpus = [dictionary.doc2bow(text) for text in corpora_documents]
        # 向量的每一个元素代表了一个word在这篇文档中出现的次数
        # 转化成tf-idf向量
        # corpus是一个返回bow向量的迭代器。下面代码将完成对corpus中出现的每一个特征的IDF值的统计工作
        tfidf_model = models.TfidfModel(corpus)
        corpus_tfidf = [tfidf_model[doc] for doc in corpus]
        # 转化成lsi向量
        lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=50)
        corpus_lsi = [lsi[doc] for doc in corpus]
        similarity_lsi = Similarity('Similarity-Lsi-index', corpus_lsi, num_features=400, num_best=5)
        #  1.测试数据
        for test_data_1 in self.nfunData:
            test_cut_raw_1 = jieba.lcut(test_data_1)
            # 2.转换成bow向量 # [(51, 1), (59, 1)]，即在字典的52和60的地方出现重复的字段，这个值可能会变化
            test_corpus_3 = dictionary.doc2bow(test_cut_raw_1)
            # 3.计算tfidf值  # 根据之前训练生成的model，生成query的TFIDF值，然后进行相似度计算
            test_corpus_tfidf_3 = tfidf_model[test_corpus_3]
            #  4.计算lsi值
            test_corpus_lsi_3 = lsi[test_corpus_tfidf_3]
            #  返回最相似的样本材料,(index_of_document, similarity) tuples
            for i, l in enumerate(similarity_lsi[test_corpus_lsi_3]):
                if l[1] > 0.8:
                    Result.append([self.funData[l[0]], test_data_1])
                if i > 1:
                    break
        return Result
