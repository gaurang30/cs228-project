import disconnect
import numpy as np
import time
print("*******************Disconnect*******************")
marks = 0
with open('testcases-small.txt','r') as f:
    for i in range(5):
        line  = f.readline().split()
        s = int(line[0])
        t = int(line[1])
        ans = int(line[2])
        graph = []
        for j in range(int(line[3])):
            line = f.readline().split()
            graph.append((int(line[0]),int(line[1])))
        num = disconnect.find_minimal( graph, s, t )
        #----------------introduced len() in the autograder as our function returns set of edges and not number--------------------
        if len(num)==ans:
            result="Passed"
            marks += 2
        else:
            result="Failed"
        print("Testcase {}:".format(i+1),result)
if marks!=0:
    tot_time = 0
    with open('testcases-large.txt','r') as f:
        for i in range(5):
            line  = f.readline().split()
            s = int(line[0])
            t = int(line[1])
            ans = int(line[2])
            graph = []
            for j in range(int(line[3])):
                line = f.readline().split()
                graph.append((int(line[0]),int(line[1])))
            t1=time.time()
            num = disconnect.find_minimal( graph, s, t )
            t2=time.time()
            if len(num)==ans:
                result="Passed"
                marks += 2
            else:
                result="Failed"
            tot_time += t2-t1
            print("Testcase {}:".format(i+6),result)
print("Marks for correctness = {}".format(marks),"/ 20 marks")
print("Total time (5 marks) = {}".format(tot_time))
print("************************************************")


