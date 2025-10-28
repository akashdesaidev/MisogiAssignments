from typing import DefaultDict

def analyze_numbers(nums: list[int]) -> dict: 
    sum=0
    mode=nums[0]
    nums.sort()

    freq = DefaultDict(int)

    for i in nums:
        sum+=i 
        freq[i]=freq[i]+1


    for i in freq:
        if freq[i]>mode:
            mode = i
    return {"mean": sum/len(nums), "median": nums[(len(nums)//2)], "mode": mode}

