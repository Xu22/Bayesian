import numpy as np
file = open('watermelon3.0.csv')
filedata = [line.strip('\n').split(',')[1:] for line in file]
idx1 = filedata[0].index('密度')
idx2 = filedata[0].index('含糖率')
for i in range(1, len(filedata)):
    filedata[i][idx1] = float(filedata[i][idx1])
    filedata[i][idx2] = float(filedata[i][idx2])
filedata = filedata[1:]
def fit(filedata, lapula_correct=True):
    diff_class = {i: set() for i in range(len(filedata[0]))}
    for raw in filedata:
        for j in range(len(raw)):
            diff_class[j].add(raw[j])
    count = {}
    for raw in filedata:
        for j in range(len(raw)):
            label = raw[-1]
            # discrete attribute
            if type(raw[j]) is not float:
                tup = (raw[j], label)
                count[tup] = (count.get(tup, [0])[0] + 1, len(diff_class[j]))
                # continuous attribute
            else:
                tup = (j, label)
                if tup not in count:
                    count[tup] = [raw[j]]
                else:
                    count[tup].append(raw[j])
    prob = {}
    total_case = len(filedata)
    for i in count:
        if type(count[i]) is list:
            mean = np.mean(count[i])
            std = np.std(count[i])
            # std = np.std(count[i], ddof=1)
            prob[i] = (mean, std)
        else:
            x, c = i
            if lapula_correct:
                if x == c:
                    prob[x] = float(count[i][0] + 1) / (total_case + count[i][1])
                else:
                    prob[i] = float(count[i][0] + 1) / (count[(c, c)][0] + count[i][1])
            else:
                if x == c:
                    prob[x] = float(count[i][0]) / total_case
                else:
                    prob[i] = float(count[i][0]) / count[(c, c)][0]
    return prob
def predict(data, prob):
    label = ['是', '否']
    p1, p2 = prob[label[0]], prob[label[1]]
    val = [np.log(p1), np.log(p2)]
    # val = [p1, p2]
    for i in data:
        for j in range(2):
            if type(i) is float:
                idx = data.index(i)
                tup = (idx, label[j])
                mean, std = prob[tup]
                p = np.exp(-(i - mean) ** 2 / (2 * std ** 2)) / (np.sqrt(2 * np.pi) * std)
            else:
                tup = (i, label[j])
                p = prob[tup]
            val[j] += np.log(p)
            # val[j] *= p
    return max(label, key=lambda x: val[label.index(x)])
prob = fit(filedata)
test_data = ['青绿', '蜷缩', '浊响', '清晰', '凹陷', '硬滑', 0.697, 0.460]
res = predict(test_data, prob)
print('res', res)
