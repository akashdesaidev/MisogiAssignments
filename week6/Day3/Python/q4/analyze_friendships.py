from collections import Counter
def analyze_friendships():
    faceBook_friends={"akash","alice","bob","charlie","david","eve","frank","grace","henry"}
    instagram_friends={"vikash","bob","charlie","david","eve","frank","grace","henry"}
    twitter_friends={"alice","david","frank","grace","henry"}
    linkedin_friends={"alice","charlie","david","eve","grace","henry"}
    combined = list(faceBook_friends)+list(instagram_friends)+list(twitter_friends)+list(linkedin_friends)
    count=Counter(combined)
    return {
        "All_Platforms":set(faceBook_friends|instagram_friends|twitter_friends|linkedin_friends),
        "facebook_only":set(faceBook_friends-instagram_friends-twitter_friends-linkedin_friends),
        "instagram_or_twitter":set(instagram_friends|twitter_friends),
        "total_unique": len(set(faceBook_friends|instagram_friends|twitter_friends|linkedin_friends)),
        "exactly_2_platform":{k: v for k,v in count.items() if v==2}
    }

result =analyze_friendships()
print(result.get("All_Platforms"))
print(result.get("facebook_only"))
print(result.get("instagram_or_twitter"))
print(result.get("total_unique"))
print(result.get("exactly_2_platform"))