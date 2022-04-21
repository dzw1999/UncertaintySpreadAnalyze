# 2.
# 肖妍红师姐标注的关联关系中的需求编号和郭维泽师兄那边的编号不一致，所以需要找到对应的gwz的编号（因为最后用的是gwz师兄的那一套）
import json
import csv

relafile = r"C:\Users\wang9\OneDrive\文档\杂-od\小论文\data\gwz新\gannt_cos.csv"
srefile = r"C:\Users\wang9\OneDrive\文档\杂-od\小论文\data\gwz新\GANNT.json"
outfile = r"C:\Users\wang9\OneDrive\文档\杂-od\小论文\data\gwz新\relations\GANNT_fin.txt"
Res = []
sen2Re = {}
resstr = ""
def readStructedRes():
    with open(srefile) as fin:
        Res = json.load(fin)
    for re in Res:
        sen = re[':'].lower()
        if sen in sen2Re.keys():
            print("%s and %s dup" %(re['#'], sen2Re[sen]['#']))
            continue
        sen2Re[sen] = re

def find_right_no():
    global resstr
    with open(relafile) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        index = 0
        # 直接自动去掉了header并且转成了字符串组成的列表
        # 需要注意的是gannt和pure的csv的字段顺序是不一样的
        for row in f_csv:
            # if index < 5:
            #     # print(row[0], row[-3])
            #     print(row)
            id = row[0]
            req1_id = row[1]
            req1 = row[2].lower()
            req2_id = row[3]
            req2 = row[4].lower()
            label = row[6]
            index+=1
            if label not in ['1', '3']:
                continue
            if req1 not in sen2Re.keys():
                print("{} rela req1 not in", id)
            elif req2 not in sen2Re.keys():
                print("{} rela req2 not in", id)
            else:
                resstr += sen2Re[req1]["#"] + " " + sen2Re[req2]["#"] + " " + label + "\n"
    with open(outfile, "w") as fout:
        fout.write(resstr)

if __name__ == "__main__":
    readStructedRes()
    find_right_no()
    '''
    FR-5-2 and FR-5-1 dup
    `FR-9-2 and FR-9-1 dup
    FR-24 and FR-23 dup
    FR-25 and FR-23 dup
    FR-27 and FR-26 dup
    FR-46-2 and FR-46-1 dup
    FR-63-2 and FR-63-1 dup
    FR-82-2 and FR-82-1 dup
    FR-84-2 and FR-84-1 dup
    {} rela req2 not in 3844
    {} rela req2 not in 1743
    {} rela req2 not in 2357
    {} rela req2 not in 4368
    {} rela req2 not in 2195
    {} rela req1 not in 2718
    {} rela req2 not in 1757
    {} rela req1 not in 1828
    {} rela req2 not in 2324
    {} rela req2 not in 1639
    {} rela req2 not in 2356
    {} rela req1 not in 1815
    '''