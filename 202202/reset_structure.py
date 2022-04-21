# 这个文件是为了统计新的gwz数据的需求集合的结构 即对于每个set 有多少条目 平均含有多少单词 gwz_count
# 后来加入了对于旧的数据集的统计 tjh_count
# 后来加入了对于OPEN数据集的统计 open_count
import json
import os

def gwz_count():
    testF = []
    filename = "GANNT.json"
    refolder = r"C:\Users\wang9\OneDrive\文档\杂-od\小论文\data\gwz新\\"
    SReFile = refolder + filename
    with open(SReFile, "r", encoding='UTF-8') as fin:
        testF = json.load(fin)

    i = 0
    words = 0
    for req in testF:
        i += 1
        text = req[':']
        words += text.count(" ") + 1
    print("{}数据集的 需求数目是{} 平均单词数量是{}".format(filename, i, words/i))

def tjh_count():
    refolder = r"C:\Users\wang9\OneDrive\文档\杂-od\小论文\data\tjh旧\tjhuse\\"
    filename = "warc"
    SReFile = refolder + filename + r"\all.txt"
    with open(SReFile, "r", encoding='UTF-8') as fin:
        lines = fin.readlines()
        i = 0
        words = 0
        for line in lines:
            if line == "\n":
                continue
            words += line.count(" ") + 1
            i += 1
        print("{}数据集的 需求数目是{} 平均单词数量是{}".format(filename, i, words / i))

def open_count():
    file_dir = r"C:\Users\wang9\Desktop\gradesign\use\docs\out2\1_4genia"
    files = os.listdir(file_dir)

    numOfRe = 0
    numOfWords = 0

    for file in files:
        filein =file_dir +"\\" +file
        with open(filein, "r", encoding='UTF-8') as fin:
            for line in fin.readlines():
                nwords = line.count(" ") + 1
                if nwords < 4:
                    continue
                numOfRe += 1
                numOfWords += nwords
        print("inall {} re {} words ave {:.2f}".format(numOfRe, numOfWords, numOfWords / numOfRe))

if __name__ == "__main__":
    open_count()
