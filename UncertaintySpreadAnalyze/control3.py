# 根据control2改写，目的是：
# 1.读取 处理新的数据
# 2，既能自动生成模糊范围，也能读取已有的标注结果

from UncertaintySpreadAnalyze import data
import stanza
from UncertaintyDetectInText import getSpeculativeWord
from UncertaintyDetectInText import getscope
from UncertaintySpreadAnalyze import demo
import re
import pprint
import json
import demjson
from typing import List


class myRE:
    def __init__(self, FRDL):
        # 六元组
        self.FRDL = FRDL

        # 自身有没有模糊性
        self.isUncertain = False

        # 如果有，模糊的范围，是一个子句
        self.scope = ""

        # 0代表没有传播，1代表前提依赖正向传播，2代表前提依赖逆向传播
        # 3表示交互正向 4表示交互逆向
        self.spread = 0

        # 传播源头的id
        self.sourceid = ""

    def getF(self):
        return self.FRDL

    def getID(self):
        return self.FRDL['#']


def tokenizeSen(text):
    nlp = stanza.Pipeline('en', use_gpu=True, processors='tokenize', tokenize_no_ssplit=True)
    words = []
    sen = nlp(text).sentences[0]
    for word in sen.words:
        words.append(word.text)
    return " ".join(words)

# 自动化生成模糊范围
def getREs(testF: List):
    global myREs
    allre = ""
    for s in testF:
        text = s[':']
        allre += text
        allre += "\n\n\n"
    allcue = getSpeculativeWord.getCues(allre)
    i = 0
    for cueinfo in allcue:
        text = cueinfo[0]
        cues = cueinfo[1]
        re = testF[i]
        tRE = myRE(re)
        id = re['#']
        i += 1
        if cues:
            tRE.isUncertain = True
            for cue in cues:
                scope = getscope.anno_sentence(text, cue)
                tRE.scope += " ".join(scope) + " "
        myREs[id] = tRE

# 读取手动标注的作为范围
def getREs_goldscope(testF: List):
    global myREs
    for re in testF:
        tRE = myRE(re)
        id = re['#']
        if id in scopes.keys():
            tRE.isUncertain = True
            tRE.scope = scopes[id]['scope']
        myREs[id] = tRE


def analyzeSpread():
    def checkinscope(s: str, scope: str, type: str):
        def rim(s: str):
            return s.replace("[", "").replace("]", "").replace(" ", "").lower()

        scope = scope.lower().replace(" ", "")
        l1 = []
        s1 = set()
        if type == "output" or type == "input":
            entities = s["()"]
            for entity in entities:
                ss = entity['entity']
                l1.append(ss)
        elif type == "event":
            events = s['()']
            for event in events:
                flag = False
                if "operation" in event.keys():
                    flag |= checkinscope(event['operation'], scope, "operation")
                if "input" in event.keys():
                    flag |= checkinscope(event['input'], scope, "input")
                if "output" in event.keys():
                    flag |= checkinscope(event['output'], scope, "output")
                return flag
        elif type == "operation":
            ss = s["operation"]
            l1.append(ss)
        else:
            print("there is no such element")
            return False
        for s in l1:
            if s != "":
                s1.add(rim(s))
        for s in s1:
            if s in scope:
                return True
        return False

    for r in result:
        sourceRE = myREs[r['id1']]
        targetRE = myREs[r['id2']]
        if not (sourceRE.isUncertain or targetRE.isUncertain):
            continue
        sre = sourceRE.getF()
        tre = targetRE.getF()
        if r['relationType'] == '1':
            if sourceRE.isUncertain:
                if 'operation' not in sre.keys():
                    print("rela 1 - {} TO {} operation not in sre".format(r['id1'], r['id2']))
                elif checkinscope(sre['operation'], sourceRE.scope, "operation"):
                    targetRE.spread = 1
                    targetRE.sourceid = sourceRE.getID()
            if targetRE.isUncertain:
                if 'event' not in tre.keys():
                    print("rela 1 - {} TO {} event not in tre".format(r['id1'], r['id2']))
                elif checkinscope(tre['event'], targetRE.scope, "event"):
                    sourceRE.spread = 2
                    sourceRE.sourceid = targetRE.getID()

        elif r['relationType'] == '3':
            if sourceRE.isUncertain:
                if 'output' not in sre.keys():
                    print("rela 3 - {} TO {} output not in sre".format(r['id1'], r['id2']))
                elif checkinscope(sre['output'], sourceRE.scope, "output"):
                    targetRE.spread = 3
                    targetRE.sourceid = sourceRE.getID()
            if targetRE.isUncertain:
                if 'input' not in tre.keys():
                    print("rela 3 - {} TO {} operation not in tre".format(r['id1'], r['id2']))
                elif checkinscope(tre['input'], targetRE.scope, "input"):
                    sourceRE.spread = 4
                    sourceRE.sourceid = targetRE.getID()
        else:
            pass
    analyzeres = []
    for re in myREs.values():
        reJson = {}
        reJson['id'] = re.getID()
        reJson['isUncertain'] = re.isUncertain
        reJson['spread'] = re.spread
        reJson['sourceid'] = re.sourceid
        analyzeres.append(reJson)

    return analyzeres

def readStructedRes():
    global testF
    with open(SReFile, "r", encoding='UTF-8') as fin:
        testF = json.load(fin)
    reSet = set()
    # 检查一下sre中有没有编号重复的
    # 最好的结果是sre中没有重复的，即使有也是-1 -2这种
    # 然后scope中呢 就对应的也按-1 -2重复来
    # 但是问题又来了 scope中一个-1可能有俩cue word 咋搞
    # 那就给他组合一下呗
    print("checking sre dup")
    for re in testF:
        if re['#'] in reSet:
            print("number ", re['#'], " dup in sre")
            continue
        reSet.add(re['#'])

def myreadRelations():
    fin = open(RelationFile, "r", encoding='UTF-8')
    lines = fin.readlines()
    fin.close()
    for line in lines:
        if line == "\n":
            continue
        contents = line.split(" ")
        if len(contents) != 3:
            print("this line:", line, " wrong")
            continue
        id1 = contents[0]
        id2 = contents[1]
        relationType = contents[2]
        if relationType[-1] == "\n":
            relationType = relationType[0:-1]
        rela = {}
        rela['id1'] = id1
        rela['id2'] = id2
        rela['relationType'] = relationType
        result.append(rela)

def readScope():
    global scopes
    with open(scopeFile, "r", encoding='UTF-8') as fin:
        allscope = json.load(fin)
    scopeSet = set()
    # 检查一下scope中有没有编号重复的
    # 转化成key-value的形式
    print("checking scope dup")
    for scope in allscope:
        if scope['sentence_id'] in scopeSet:
            print("number ", scope['sentence_id'], " dup")
            continue
        scopeSet.add(scope['sentence_id'])
        if scope['scope'] == "":
            continue
        scopes[scope['sentence_id']] = scope

testF = []
result = []
scopes = {}
myREs = {}

filename = "GANNT"

SReFile = r"C:\Users\wang9\OneDrive\文档\杂-od\小论文\data\gwz新\gold standard changed\jiegouhua\\" + filename + ".json"
RelationFile = r"C:\Users\wang9\OneDrive\文档\杂-od\小论文\data\gwz新\relations2\\" + filename + ".txt"
scopeFile = r"C:\Users\wang9\OneDrive\文档\杂-od\小论文\data\gwz新\gold standard changed\uncertainty\\" + filename + ".json"
outFile = r"C:\Users\wang9\OneDrive\文档\杂-od\小论文\data\gwz新\res\spread\\" + filename + ".json"

def startAnalyze(srefile: str, relafile: str):
    global SReFile, RelationFile
    SReFile = srefile
    RelationFile = relafile
    readStructedRes()
    # readRelations()
    getREs(testF)
    return analyzeSpread()


if __name__ == "__main__":
    readStructedRes()
    myreadRelations()
    readScope()
    getREs(testF)
    # getREs_goldscope(testF)
    res = analyzeSpread()
    with open(outFile, 'w') as fout:
        json.dump(res, fout, indent = 4)