def lengthOfLongestSubstring(s: str) -> int:
    # Create a set to store the characters that have been seen so far
    # 'eedde'
    seen = set()
    # Create a variable to store the length of the longest substring without repeating characters
    max_length = 0
    # Create two pointers to keep track of the current substring
    left = 0
    right = 0
    # Loop through the characters in the string
    while right < len(s):
        # If the current character has not been seen before, add it to the set and move the right pointer one character to the right
        if s[right] not in seen:
            seen.add(s[right])
            right += 1
            # Update the maximum length of the substring if necessary
            max_length = max(max_length, right - left)
        # If the current character has been seen before, remove the character at the left pointer from the set and move the left pointer one character to the right
        else:
            seen.remove(s[left])
            left += 1
    # Return the length of the longest substring without repeating characters
    return max_length, seen
