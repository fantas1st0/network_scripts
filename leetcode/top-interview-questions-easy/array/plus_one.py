"""
Given a non-empty array of decimal digits representing a non-negative integer, increment one to the integer.

The digits are stored such that the most significant digit is at the head of the list, and each element in the array contains a single digit.

You may assume the integer does not contain any leading zero, except the number 0 itself.

Example 1:

Input: digits = [1,2,3]
Output: [1,2,4]
Explanation: The array represents the integer 123.
Example 2:

Input: digits = [4,3,2,1]
Output: [4,3,2,2]
Explanation: The array represents the integer 4321.
Example 3:

Input: digits = [0]
Output: [1]
"""

def main(digits):
	index = -1
	setdig = set(digits)
	if int(list(setdig)[0]) == 9 and len(list(setdig)) == 1:
		digits = [0] * (len(digits) + 1 )
		digits[0] = 1
		return(digits)
	for num in digits:
		if digits[index] != 9:
			digits[index] = digits[index] + 1
			return(digits)
		if digits[index] == 9:
			digits[index] = 0
			if digits[index - 1] != 9:
				digits[index - 1] = digits[index - 1] + 1
				return(digits)
			elif digits[index - 1] == 9:
				digits[index - 1] = 0
				index = index - 2
	return(digits)

if __name__ == "__main__":
	digits = [8, 9, 9, 9]
	number = main(digits)
	print(number)
