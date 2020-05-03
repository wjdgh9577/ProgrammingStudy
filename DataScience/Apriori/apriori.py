import sys
from itertools import combinations

def init():
    #Exception
    if len(sys.argv) != 4:
        print("Input \"apriori.py (min_sup) (input.txt) (output.txt)\"")
        exit(1)

    #Get minimum support
    min_sup = float(sys.argv[1])/100

    #Read transaction data and set DB
    f = open(sys.argv[2], 'r')
    transactions = []
    lines = f.readlines()
    for line in lines:
        s = set(map(int, line.split()))
        transactions.append(s)
    f.close()

    return min_sup, transactions

def CreateCandidates(L, k, transactions):
    C = set()

    if k == 1:
        #Make candidate itemsets of size 1
        for transaction in transactions:
            for item in transaction:
                C.add(frozenset({item}))
    else:
        #Self-Joining
        #Make candidate itemsets of size k
        for itemset1 in L:
            for itemset2 in L:
                unionset = itemset1 | itemset2
                if len(unionset) == k:
                    C.add(frozenset(unionset))
    return C

def Pruning(C, transactions, min_sup, frequent):
    L = set()

    #Scan and count frequent
    for item in C:
        for transaction in transactions:
            if item.issubset(transaction):
                if item in frequent:
                    frequent[item] += 1
                else:
                    frequent[item] = 1
                    
    #Make frequent itemsets of size K
    for item in C:
        if frequent[item]/len(transactions) >= min_sup:
            L.add(item)
    return L

def GetSubsets(item):
    l = []
    for i in range(1, len(item)+1):
        l.append(list(map(frozenset, combinations(item, i))))
    return l
    
def Apriori():
    #Initialize
    min_sup, transactions = init()
    L_k = set({0})
    frequent = {}
    total = {}
    
    #Iteration
    k = 1
    while len(L_k) != 0:
        C_k = CreateCandidates(L_k, k, transactions)
        L_k = Pruning(C_k, transactions, min_sup, frequent)
        if len(L_k) != 0:
            total[k] = L_k
        k += 1
    
    #Get support and confidence
    f = open(sys.argv[3], 'w')
    for i in range(1, len(total)+1):
        for item in total[i]:
            for subsets in GetSubsets(item):
                for subset in subsets:
                    if len(subset) != 0 and len(subset) != len(item):
                        difference = item.difference(subset)
                        support = round(100*frequent[item]/len(transactions), 2)
                        confidence = round(100*frequent[item]/frequent[subset], 2)

                        output = str(set(subset))+'\t'+str(set(difference))+'\t'+str(support)+'\t'+str(confidence)+'\n'
                        f.writelines(output)
    f.close()

if __name__ == "__main__":
    Apriori()
