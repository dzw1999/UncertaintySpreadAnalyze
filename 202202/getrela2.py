# 3.
# 肖妍红师姐给我发了gannt的对应上的csv 需要我自己提取一下就好了
import json
import csv
relafile = r"C:\Users\wang9\OneDrive\文档\杂-od\小论文\data\gwz新\gannt_unified.csv"
outfile = r"C:\Users\wang9\OneDrive\文档\杂-od\小论文\data\gwz新\relations2\GANNT.txt"


resstr = ""
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
        req2_id = row[2]
        label = row[5]
        index += 1
        if label not in ['1', '3']:
            continue
        resstr += req1_id + " " + req2_id + " " + label + "\n"
    with open(outfile, "w") as fout:
        fout.write(resstr)

