def insertionsort(K):
    n=len(K)
    i=1
    while(i<n):
        key=K[i]
        j=i-1
        while(K[j]>key and j>=0):            
            K[j+1]=K[j]
            j=j-1
        K[j+1]=key
        i=i+1
    print(K)

K=[3,2,1,4,5,-1,4]
insertionsort(K)
