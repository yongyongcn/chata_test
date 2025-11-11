
from typing import List
def twoSum( nums: List[int], target: int) -> List[int]:
    dict_nums={ nums[0] :0}
    for i in range(1, len(nums)):
        if target-nums[i] not in dict_nums:
                dict_nums[nums[i]]=i
        else:
            return[dict_nums[target-nums[i]],i]
nums=[2,7,11,15]
target=9
rs=twoSum(nums,target)
print(rs)

# print(twoSum(None,nums,target))