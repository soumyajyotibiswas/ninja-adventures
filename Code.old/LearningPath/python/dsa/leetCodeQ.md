
# LeetCode Questions

Problems as listed [here](https://github.com/ombharatiya/FAANG-Coding-Interview-Questions#faang-must-do-problems).

## TOC

- [LeetCode Questions](#leetcode-questions)
  - [TOC](#toc)
  - [Two Sum - LeetCode](#two-sum---leetcode)
    - [Brute force](#brute-force)
    - [Dictionary](#dictionary)
  - [Longest Substring Without Repeating Characters - LeetCode](#longest-substring-without-repeating-characters---leetcode)
    - [Sliding Window](#sliding-window)
  - [Longest Palindromic Substring - LeetCode](#longest-palindromic-substring---leetcode)
    - [Brute force](#brute-force-1)
  - [Container With Most Water - LeetCode](#container-with-most-water---leetcode)
    - [Brute force](#brute-force-2)
    - [Two-pointer approach](#two-pointer-approach)
  - [Three Sum](#three-sum)
    - [Two pointer](#two-pointer)


## [Two Sum - LeetCode](https://leetcode.com/problems/two-sum/)

### Brute force

The time complexity of this algorithm is O(n^2), since it uses two nested loops to check every possible pair of numbers in the array. The space complexity is O(1), since the function uses only a constant amount of additional memory, regardless of the size of the input.

```Python
# Function to return indices of two numbers that add up to target
def two_sum(nums, target):
  # Loop through the array
  for i in range(len(nums)):
    # Loop through the remaining elements
    for j in range(i+1, len(nums)):
      # Check if the two elements add up to the target
      if nums[i] + nums[j] == target:
        # Return the indices
        return (i, j)

# Test the function
print(two_sum([1, 2, 3, 4], 5))  # Should print (0, 3)

```

### Dictionary

The time complexity of this algorithm is O(n), since it uses only a single loop to traverse the array. The space complexity is O(n), since the function uses a dictionary to store the elements and their corresponding indices, which could take up to O(n) additional memory.

```Python
# Function to return indices of two numbers that add up to target
def two_sum(nums, target):
  # Create an empty dictionary
  indices = {}

  # Loop through the array
  for i in range(len(nums)):
    # Check if target - current element is in the dictionary
    if target - nums[i] in indices:
      # Return the indices
      return (indices[target - nums[i]], i)
    else:
      # Add the current element and its index to the dictionary
      indices[nums[i]] = i

# Test the function
print(two_sum([1, 2, 3, 4], 5))  # Should print (0, 3)

```

## [Longest Substring Without Repeating Characters - LeetCode](https://leetcode.com/problems/longest-substring-without-repeating-characters/)

### Sliding Window

The time complexity of this algorithm is O(n), where n is the length of the input string. This is because we loop through the characters in the input string once and do a constant amount of work for each character.

The space complexity of this algorithm is O(k), where k is the length of the longest substring without repeating characters. This is because we store each character we see in a set, so the space used is proportional to the length of the longest substring without repeating characters.

The algorithm used in this solution is called a sliding window algorithm. This algorithm maintains a set of characters that have been seen so far and a window that slides from the start of the string to the end of the string. As the window slides, the algorithm keeps track of the longest substring without repeating characters that it has seen so far. When it encounters a character that has already been seen, it removes the character at the start of the window from the set and increments the start of the window, continuing to slide the window until it encounters a character that has not been seen before.

```Python
def longest_substring(s: str) -> int:
    # create an empty set to store the characters we've seen so far
    seen = set()

    # initialize the length of the longest substring to 0
    longest = 0

    # initialize the start and end indices to 0
    start = 0
    end = 0

    # loop through the characters in the string
    while end < len(s):
        # if the current character has not been seen before, add it to the set
        if s[end] not in seen:
            seen.add(s[end])
            end += 1
            longest = max(longest, end - start)
        # if the current character has been seen before, remove the character at the start index from the set
        # and increment the start index
        else:
            seen.remove(s[start])
            start += 1

    # return the length of the longest substring
    return longest

```

## [Longest Palindromic Substring - LeetCode](https://leetcode.com/problems/longest-palindromic-substring/)

### Brute force

The time complexity of this solution is `O(n^2)`, where `n` is the length of the input string `s`. This is because, in the worst case, the function will iterate over every character in the string and, for each character, it will expand the palindrome to its maximum length by moving the left and right indices outwards until they reach the end of the string.

The space complexity of this solution is `O(1)`, since the function only uses a few variables that do not depend on the input size. This means that the function uses a constant amount of memory, regardless of the size of the input string.

The solution uses a brute-force algorithm to find the longest palindromic substring in the input string. This means that it simply checks every possible substring of the input string to see if it is a palindrome, and it keeps track of the longest palindrome it has seen so far.

To do this, the function iterates over each character in the input string and checks for palindromes with odd lengths centered at that character, as well as palindromes with even lengths centered between that character and the next character. For each of these cases, it uses a helper function called `_palindrome_at()` to expand the palindrome until it reaches the end of the string or until the characters at the left and right indices are no longer the same. The function then returns the palindrome, not including the characters it moved past.

This algorithm is not the most efficient way to solve the problem, but it is relatively simple to understand and implement, which makes it a good starting point for solving this problem. There are other, more efficient algorithms that can be used to solve this problem, such as dynamic programming or suffix tree algorithms. These algorithms can solve the problem in `O(n)` time, which is significantly faster than the brute-force approach.

```Python
def longest_palindromic_substring(s: str) -> str:
  # Edge case: empty string
  if not s:
    return ""

  # Initialize the result to be the first character of the string
  result = s[0]

  # Iterate over the characters in the string
  for i, c in enumerate(s):
    # Check for palindromes with odd lengths centered at this character
    p = _palindrome_at(s, i, i)
    if len(p) > len(result):
      result = p

    # Check for palindromes with even lengths centered at this character and the next character
    p = _palindrome_at(s, i, i + 1)
    if len(p) > len(result):
      result = p

  return result

def _palindrome_at(s: str, left: int, right: int) -> str:
  # While the left and right indices are within the bounds of the string
  # and the characters at those indices are the same,
  # expand the palindrome by moving the left and right indices outward
  while left >= 0 and right < len(s) and s[left] == s[right]:
    left -= 1
    right += 1

  # Return the palindrome, not including the characters we moved past
  return s[left + 1:right]

```

## [Container With Most Water - LeetCode](https://leetcode.com/problems/container-with-most-water/)

### Brute force

The time complexity of this solution is O(n^2)

```Python
def maxArea(height):
  max_area = 0
  for i in range(len(height)):
    for j in range(i + 1, len(height)):
      # Calculate the area between the ith and jth lines
      width = j - i
      min_height = min(height[i], height[j])
      area = width * min_height
      # Update max_area if the current area is greater
      max_area = max(max_area, area)
  return max_area

```

### Two-pointer approach

The time complexity of this solution is O(n) since we iterate over all elements of the array once. The space complexity is O(1) since we only use constant space.

The algorithm used in this solution is called two-pointer approach. This algorithm is a simple and efficient way to solve problems involving two pointers that move towards the center. In this particular problem, we use two pointers to keep track of the left and right endpoints of the container and move the pointer with the shorter height towards the center to find the maximum possible area for the container.

```Python
def maxArea(height):
    # Initialize maximum area
    max_area = 0

    # Set the left and right pointer to the first and last element of the array
    left = 0
    right = len(height) - 1

    # Loop until left and right pointers meet
    while left < right:
        # Calculate the area by multiplying the minimum height of the two lines
        # by the distance between them
        area = min(height[left], height[right]) * (right - left)

        # Update maximum area if this area is greater
        max_area = max(max_area, area)

        # Move the pointer with the shorter height towards the center
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_area

```

## [Three Sum](https://leetcode.com/problems/3sum/)

### Two pointer

The time complexity of this solution is O(n^2), where n is the length of the input array nums. This is because the solution uses the two-pointer technique to find the triplets, which takes O(n^2) time in the worst case.

The space complexity of this solution is O(1), because it only uses a constant amount of space to store the pointers and the result. It does not use any additional space proportional to the size of the input array.

The algorithm used in this solution is the two-pointer technique. It is a common technique used to solve problems involving arrays where we need to find pairs or triplets that satisfy some condition.

The two-pointer technique works by first sorting the array in the desired order (ascending or descending), then using two pointers to iterate over the array and find the elements that satisfy the given condition. The left pointer starts at the beginning of the array and the right pointer starts at the end of the array. Depending on the condition, the pointers are moved towards each other or away from each other until they meet or pass each other.

In this specific problem, we are looking for triplets that sum up to zero. So, the algorithm first sorts the array in ascending order, then iterates over the array and uses the two-pointer technique to find the remaining two elements of the triplet that sum up to zero. It moves the pointers towards each other if the sum is greater than zero, and away from each other if the sum is less than zero. It skips the duplicate elements to avoid duplicate triplets in the result.

```Python
def three_sum(nums):
    # sort the array in ascending order
    nums.sort()

    # create an empty list to store the result
    result = []

    # iterate over the array, starting from the first element
    for i in range(len(nums)):
        # get the current element
        num = nums[i]

        # check if the current element is the same as the previous element
        # we do this to avoid duplicate triplets
        if i > 0 and num == nums[i-1]:
            continue

        # initialize two pointers for the remaining elements
        left = i + 1
        right = len(nums) - 1

        # iterate until the pointers meet
        while left < right:
            # calculate the sum of the current triplet
            curr_sum = num + nums[left] + nums[right]

            # check if the sum is zero
            if curr_sum == 0:
                # if the sum is zero, add the triplet to the result
                result.append([num, nums[left], nums[right]])

                # move the left and right pointers
                left += 1
                right -= 1

                # skip the duplicate elements
                while left < right and nums[left] == nums[left-1]:
                    left += 1
                while left < right and nums[right] == nums[right+1]:
                    right -= 1
            # if the sum is positive, move the right pointer
            elif curr_sum > 0:
                right -= 1
            # if the sum is negative, move the left pointer
            else:
                left += 1

    return result
```