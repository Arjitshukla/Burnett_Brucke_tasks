# • Reverse a sentence.

def reverse_sentence(sentence):
    # Handle empty input
    if not sentence or not sentence.strip():
        return "Error: Input sentence cannot be empty."

    # Reverse the sentence characters
    reversed_sentence = sentence[::-1]
    return reversed_sentence


# Take input from user
sentence = input("Enter a sentence: ")
result = reverse_sentence(sentence)

print(result)


# Check whether a word is a palindrome.
def is_palindrome(word):
    # Handle empty input
    if not word or not word.strip():
        return "Error: Input word cannot be empty."

    # Normalize the word to lowercase for case-insensitive comparison
    normalized_word = word.lower()

    # Check if the word is a palindrome
    if normalized_word == normalized_word[::-1]:
        return f"'{word}' is a palindrome."
    else:
        return f"'{word}' is not a palindrome."

# Take input from user
word = input("Enter a word: ")

# Call function and display result
result = is_palindrome(word)
print(result)


# • Count vowels and consonants

def count_vowels_consonants(text):
    # Handle empty input
    if not text or not text.strip():
        return "Error: Input text cannot be empty."

    # Initialize counters
    vowels = 0
    consonants = 0

    # Define vowel set
    vowel_set = set("aeiouAEIOU")

    # Count vowels and consonants
    for char in text:
        if char.isalpha():  # Check if character is a letter
            if char in vowel_set:
                vowels += 1
            else:
                consonants += 1

    return f"Vowels: {vowels}, Consonants: {consonants}"
 
text = input("Enter a text: ")
result = count_vowels_consonants(text)
print(result)



# Count total words.

def count_total(text):

    # Handle empty input
    if not text or not text.strip():
        return "Error: Input text cannot be empty."

    # Count total words
    words = text.split()
    count = len(words)

    return count


text = input("Enter a text: ")
total_word = count_total(text)

print(f"Total words: {total_word}")




# Count character frequency.

def count_character_frequency(text):
    # Handle empty input
    if not text or not text.strip():
        return "Error: Input text cannot be empty."

    # Initialize frequency dictionary
    frequency = {}

    # Count character frequency
    for char in text:
        if char.isalpha():  
            char_lower = char.lower()  # Normalize to lowercase
            frequency[char_lower] = frequency.get(char_lower, 0) + 1

    return frequency

text ="python programming"
result = count_character_frequency(text)
print(result)



# Find the first non-repeating character.

def first_non_repeating_character(text):
    # Handle empty input
    if not text or not text.strip():
        return "Error: Input text cannot be empty."

    # Initialize frequency dictionary
    frequency = {}

    # Count character frequency
    for char in text:
        if char.isalpha():  
            char_lower = char.lower()  # Normalize to lowercase
            frequency[char_lower] = frequency.get(char_lower, 0) + 1

    # Find the first non-repeating character
    for char in text:
        if char.isalpha():
            char_lower = char.lower()
            if frequency[char_lower] == 1:
                return f"The first non-repeating character is: '{char}'"

    return "No non-repeating character found."

text = "python programming"
result = first_non_repeating_character(text)
print(result)




# Remove extra spaces
def remove_extra_spaces(text):
    # Handle empty input
    if not text or not text.strip():
        return "Error: Input text cannot be empty."

    # Remove extra spaces
    cleaned_text = " ".join(text.split())
    return cleaned_text

text = "    Hello     Python     World    "

# Call function
result = remove_extra_spaces(text)

print(f"Cleaned text: {result}")
