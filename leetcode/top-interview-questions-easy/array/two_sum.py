"""
https://leetcode.com/explore/interview/card/top-interview-questions-easy/92/array/546/

Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
You may assume that each input would have exactly one solution, and you may not use the same element twice.
You can return the answer in any order.

Example 1:

Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Output: Because nums[0] + nums[1] == 9, we return [0, 1].
"""

def main(nums, target):
	d  = {}
	for i in range(len(nums)):
		if target - nums[i] in d:
			return i, d[target - nums[i]]
		d[nums[i]] = i

if __name__ == "__main__":
	nums = [2,7,11,15]
	target = 6 
	i, j = main(nums, target)
	print(i, j)
