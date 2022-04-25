# 1.0
# 这个文件为了生成gwz新数据对应的单一需求模糊，并且读取连老师的标注并计算准确率
# 做法是直接遍历所有需求条目，按照之前gold standard组织的形式输出检测结果，然后因为数量并不多所以直接人工比对
# 2.0
# 220421
# 连老师让我用Yanghui的baseline跑一个结果出来，与我的结果进行对比
# 为此通过缩减实现了getscope_yangui
# hopefully it will work

import stanza
from UncertaintyDetectInText import getSpeculativeWord
from UncertaintyDetectInText import getscope_yanghui
from typing import List
import json
def readStructedRes():
    global testF
    with open(SReFile,"r",encoding='UTF-8') as fin:
        testF=json.load(fin)

def getREs(testF:List):
    global result
    allre=""
    for s in testF:
        text = s[':']
        allre+=text
        allre+="\n\n\n"
    allcue=getSpeculativeWord.getCues(allre)
    i=0
    for cueinfo in allcue:
        text=cueinfo[0]
        cues=cueinfo[1]
        s=testF[i]
        id = s['#']
        i+=1
        if cues:
            for cue in cues:
                scope = getscope_yanghui.anno_sentence(text, cue)
                res = {}
                res['sentence_id'] = id
                res['sentence'] = text
                res['cue_offfset'] = cue[0]
                res["cue"] = cue[1]
                res['scope'] = " ".join(scope)
                result.append(res)
        else:
            res = {}
            res['sentence_id'] = id
            res['sentence'] = text
            res['cue_offfset'] = -1
            res["cue"] = ""
            res['scope'] = ""
            result.append(res)
    with open(outFile,"w",encoding='UTF-8') as fout:
        json.dump(result, fout, indent = 4)

result = []
testF = []
filename = "PURE.json"
refolder = r"C:\Users\wang9\OneDrive\文档\杂-od\小论文\data\gwz新\base\\"
SReFile = refolder + filename
resfolder = r"C:\Users\wang9\OneDrive\文档\杂-od\小论文\data\gwz新\res\uncertainty_yanghui\\"
outFile = resfolder + filename
if __name__ == "__main__":
    readStructedRes()
    getREs(testF)