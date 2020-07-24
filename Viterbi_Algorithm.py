import math
import numpy as np

""" Loading all the files"""
with open('emissionMatrix.txt') as file1:
    emissionMatrix = [[float(digit) for digit in a.split()] for a in file1]
with open('transitionMatrix.txt') as file2:
    transMat = [[float(x) for x in b.split()] for b in file2]
with open('initialStateDistribution.txt') as file3:
    initStateDist = [[float(y) for y in c.split()] for c in file3]
lines = open('observations.txt')
observations = lines.read().split(' ')

lit_matrix = np.zeros(shape=(27, len(observations)))
index_matrix = np.zeros(shape=(27, len(observations)), dtype=np.int)
most_likely_sequence = np.zeros(shape=(len(observations),), dtype=np.int)

# load the first column with initial value
for i in range(27):
    if observations[0] == "0":
        lit_matrix[i, 0] = math.log(initStateDist[i][0]) + math.log(emissionMatrix[i][0])
        # print("in here")
    else:
        lit_matrix[i, 0] = math.log(initStateDist[i][0]) + math.log(emissionMatrix[i][1])

# now do the rest of the table
for t in range(1, len(observations)):
    for letter in range(27):
        obs_val = 0

        if observations[t] == "0":
            obs_val = 0
        else:
            obs_val = 1

        lit_matrix[letter, t] = np.max([lit_matrix[i, t-1] + math.log(transMat[i][letter]) + math.log(emissionMatrix[letter][obs_val]) for i in range(27)])

        index_matrix[letter, t] = np.argmax([lit_matrix[i][t-1] + math.log(transMat[i][letter]) for i in range(27)])

        #print("lit mat: " + str(lit_matrix[letter, t]) + " index mat: " + str(index_matrix[letter, t]))
    print("above is from column: {}".format(t))

# the max value in the last column used to trace back
most_likely_sequence[len(observations)-1] = np.argmax([lit_matrix[j, len(observations)-1] for j in range(27)])

# start at the last element
prev = most_likely_sequence[-1]

for x in range(len(observations)-1, -1, -1):
    prev = index_matrix[prev, x]
    most_likely_sequence[x] = prev

# the 'graph' which is the message

""" The message is as follows: 'a democracy is the worst form of government except for al the others' """

count = 1
curletter = -1
for t in range(len(observations)):

    # get the current letter
    if t == 0:
        curletter = most_likely_sequence[t]

    if t != 0 and most_likely_sequence[t] == most_likely_sequence[t-1]:
        count += 1

    if t != 0 and most_likely_sequence[t] != most_likely_sequence[t-1]:
        print("{}: ".format(str(curletter)) + str(count) + chr(curletter + 97))
        curletter = most_likely_sequence[t]
        count = 1
    if t == len(observations) - 1:
        print("{}: ".format(str(curletter)) + str(count) + chr(curletter + 97))
