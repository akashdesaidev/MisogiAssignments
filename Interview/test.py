string = "Hello, World!###"
ans=""
for i in string:
    val =ord(i)
    # print(i,val)
    if (i==" "):
     ans+=" "
    elif (val>=48 and val<=57)or (val>=65 and val<=90) or(val>=97 and val<=122):
        ans+=i

print("ans",ans)
