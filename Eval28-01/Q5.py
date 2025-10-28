

ans = map(lambda x :x if((x %7!=0 and x %9==0) or (x %7==0 and x %9!=0)) else 0,list(range(1,100)))
for i in ans:
    if i !=0:
        print(i)