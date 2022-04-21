# 1.
# 只是为了测试用的
import json
testF = []
testRe1 = {}
testRe2 = {}
testStr1 = "The file is \"warc.h\"."
testStr2 = "He is called \'jason\'."
testRe1["sen1"] = testStr1
testRe1["sen2"] = testStr2
testRe2["sen1"] = testStr2
testRe2["sen2"] = testStr1
testF.append(testRe1)
testF.append(testRe2)
outfile = r"C:\Users\wang9\Desktop\old_spread_res\202202\test.json"
with open(outfile, 'w') as fout:
    json.dump(testF, fout)