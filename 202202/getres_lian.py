# 4.
# 连老师标注的模糊检测结果比较简单 需要我把他转换成可以用于后续处理的格式
# 输出两个文件夹
#   一个是json 里面含有原句子以及空出来的cue scope等 我后续自己手动填充上了
#   另一个是helper 里面是包含每个单词的索引 帮助我标注的

import json
import stanza
outdir = r"C:\Users\wang9\OneDrive\文档\杂-od\小论文\data\gwz新\uncertainty\\"
nlp = stanza.Pipeline('en', use_gpu=True, processors='tokenize', tokenize_no_ssplit=True)

def getUncertaindata():
    srefile1 = r"C:\Users\wang9\OneDrive\文档\杂-od\小论文\data\gwz新\GANNT.json"
    srefile2 = r"C:\Users\wang9\OneDrive\文档\杂-od\小论文\data\gwz新\PURE.json"
    srefile3 = r"C:\Users\wang9\OneDrive\文档\杂-od\小论文\data\gwz新\UAV.json"
    outfiles = []
    outfiles2 = []
    outfiles.append(outdir + "GANNT.json")
    outfiles.append(outdir + "PURE.json")
    outfiles.append(outdir + "UAV.json")
    outfiles2.append(outdir + "help\\" + "GANNT.txt")
    outfiles2.append(outdir + "help\\" + "PURE.txt")
    outfiles2.append(outdir + "help\\" + "UAV.txt")
    srefiles = [srefile1, srefile2, srefile3]
    for i in range(1, 3):
        with open(srefiles[i]) as fin:
            Res = json.load(fin)
            with open(outfiles[i], "w") as fout:
                with open(outfiles2[i], "w") as fout2:
                    newRes = []
                    helperres = ""
                    for re in Res:
                        newre = {}

                        newre["sentence_id"] = re['#']

                        words = []
                        helperres += re[':'] + "\n"
                        sen = nlp(re[':']).sentences[0]
                        index = 0
                        for word in sen.words:
                            words.append(word.text)
                            helperres += word.text + "\t"
                            helperres += str(index) + "\t"
                            index +=1
                        helperres += "\n\n"
                        newre["sentence"] = " ".join(words)

                        newre["cue_offfset"] = -1
                        newre["cue"] = ""
                        newre["scope"] = ""
                        newRes.append(newre)
                    json.dump(newRes, fout, indent=4)
                    fout2.write(helperres)

# 这个函数是为了标注的方便 输出每一个单词对应的Index
def getHelpcuedata():
    pass

if __name__ == "__main__":
    getUncertaindata()
    getHelpcuedata()