from collections import Counter,defaultdict 
posts=[
    {"id":1,"user":"alice","content":"love python programming!","likes":10,"tags":["python","programming","tech"]},
    {"id":2,"user":"bob","content":"learning python is fun","likes":15,"tags":["programming","tech"]},
    {"id":3,"user":"charlie","content":"python is powerful","likes":20,"tags":["python","programming","tech"]},
]
users={
   "alice":{"followers":150,"following":100},
   "bob":{"followers":100,"following":150},
   "charlie":{"followers":120,"following":130}
}   


all_tags = [tag for post in posts for tag in post['tags']]

tag_counter = Counter(all_tags)
top_tags = tag_counter.most_common(3)
print(top_tags)

# Top Posts by Likes – Use sorted() to list posts in descending order of likes.
sorted_posts=sorted(posts,key=lambda x:x.get("likes"),reverse=True)
print(sorted_posts)
