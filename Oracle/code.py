def bestTrio(friends_nodes, friends_from, friends_to):
    counter = [0 for i in range(friends_nodes+1)]
    h = [set() for i in range(friends_nodes+1)]
    result = {}
    for i,j in zip(friends_from, friends_to):
        h[i].add(j)
        h[j].add(i)
        counter[i] += 1
        counter[j] += 1
        val = (i,j)
        result[val] = 1+result.get(val,0)
        val = (j,i)
        result[val] = 1+result.get(val,0)
    ans = float('inf')
    for i in range(1, friends_nodes+1):
        for j in range(i+1, friends_nodes+1):
            f,s = h[i], h[j]
            middle = f.intersection(s)
            if i in s:
                for x in middle:
                    if x != i and x != j:
                        ans = min(ans, counter[x]+counter[i]+counter[j]-2*(result[(x,i)]+result[(x,j)]+result[(i,j)]))
    return ans if ans != float('inf') else -1
