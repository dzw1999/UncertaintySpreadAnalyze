# 对比spread的gold_standard(其实就是用标注的scope跑出来的)以及spread的res(其实就是scope是自动生成的)
import json
filename = "GANNT.json"
goldfolder = r"C:\Users\wang9\OneDrive\文档\杂-od\小论文\data\gwz新\gold standard changed\spread\\"
goldfile = goldfolder + filename
resfolder = r"C:\Users\wang9\OneDrive\文档\杂-od\小论文\data\gwz新\res\spread\\"
resfile = resfolder + filename

outfolder = r"C:\Users\wang9\OneDrive\文档\杂-od\小论文\data\gwz新\res\spread\diff\\"
outfile = outfolder + filename

gold = []
res = []
out = []
with open(goldfile, "r", encoding='UTF-8') as fin:
    gold = json.load(fin)

with open(resfile, "r", encoding='UTF-8') as fin:
    res = json.load(fin)

if len(gold) != len(res):
    print("diff len!!!")
    exit(0)

m_gold = {}
m_res = {}
for re in gold:
    m_gold[re['id']] = re['spread']
for re in res:
    id = re['id']
    if id not in m_gold.keys():
        print("{} not in gold".format(id))
        continue
    if m_gold[id] != re['spread']:
        out.append(id)

with open(outfile, "w", encoding='UTF-8') as fout:
    json.dump(out, fout, indent=4)
