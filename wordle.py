words = []

# listas separadas para tipos diferentes de letras
green_chars = []    # (letra, pos)
yellow_chars = []   # (letra, pos) - existe mas nao
grey_chars = []     # letra - letra NAO existe

def wordList():
    for i in words:
        print(i)

def getFeedback():
    feedback = input("Feedback (g=green, y=yellow, b=grey): ").strip().lower()
    for pos, (letter, fb) in enumerate(zip(dayWord, feedback)):
        if fb == "g":
            green_chars.append((letter, pos))
            print("Added", letter, "as GREEN at pos", pos)
        elif fb == "y":
            yellow_chars.append((letter, pos))
            print("Added", letter, "as YELLOW at pos", pos)
        elif fb == "b":
            # Verifica se essa letra esta na palavra sendo verde ou amarela
            letter_in_word_already = False
            for other_pos, (other_letter, other_fb) in enumerate(zip(dayWord, feedback)):
                if other_pos != pos and other_letter == letter and other_fb in ['g', 'y']:
                    letter_in_word_already = True
                    break
            
            if not letter_in_word_already:
                if letter not in grey_chars:
                    grey_chars.append(letter)
                    print("Added", letter, "as GREY (not in word)")
            else:
                print("Letter", letter, "appears elsewhere in word, not adding to grey")

with open("sorted.txt") as f:
    for line in f:
        word = line.strip()
        words.append(word)

def filterWords():
    global words
    new_words = []
    
    for w in words:
        if w == dayWord:
            print("Removed", w, "because it's the guess word")
            continue

        keep = True
        
        # Check GREEN letters (must be at exact position)
        for letter, pos in green_chars:
            if w[pos] != letter:
                print("Removed", w, "because green", letter, "not in pos", pos)
                keep = False
                break
        
        if not keep:
            continue
            
        # Check YELLOW letters (must be in word but NOT at this position)
        for letter, wrong_pos in yellow_chars:
            if letter not in w:
                print("Removed", w, "because yellow", letter, "not in word")
                keep = False
                break
            elif w[wrong_pos] == letter:
                print("Removed", w, "because yellow", letter, "at wrong pos", wrong_pos)
                keep = False
                break
        
        if not keep:
            continue
            
        # Check GREY letters (must NOT be in word at all, unless they're known to be there)
        for letter in grey_chars:
            # Count how many times this letter appears in the word
            letter_count = w.count(letter)
            
            # Count how many times this letter is known to be in the word (green + yellow)
            known_count = sum(1 for ch, _ in green_chars + yellow_chars if ch == letter)
            
            # If the word has more of this letter than we know should be there, remove it
            if letter_count > known_count:
                print("Removed", w, "because it has extra", letter, "(grey letter)")
                keep = False
                break
        
        if not keep:
            continue
            
        # Additional check: make sure the word doesn't have letters that are completely grey
        # and not offset by any green/yellow occurrences
        for letter in grey_chars:
            # If this letter is not known to be in the word at all (no green/yellow for it)
            known_occurrences = sum(1 for ch, _ in green_chars + yellow_chars if ch == letter)
            if known_occurrences == 0 and letter in w:
                print("Removed", w, "because grey letter", letter, "appears in word")
                keep = False
                break
        
        if keep:
            new_words.append(w)

    words = new_words

def suggestBestWord():
    if not words:
        return None
    
    # Score words based on how many unique letters they have
    # Prefer words with more unique letters to avoid double letter issues
    scored_words = []
    for word in words:
        # Score: number of unique letters (higher is better)
        unique_letters = len(set(word))
        # Penalty for using grey letters
        grey_penalty = sum(1 for letter in word if letter in grey_chars)
        score = unique_letters - (grey_penalty * 0.1)
        
        scored_words.append((word, score))
    
    # Sort by score descending
    scored_words.sort(key=lambda x: x[1], reverse=True)
    return scored_words[0][0]

dayWord = input("\nPlease input first word: ")
while True:
    getFeedback()
    filterWords()
    
    print(len(words), "words to choose from still.")
    
    if words:
        print("Words still in: ")
        wordList()
        best_word = suggestBestWord()
        print("You should try:", best_word)
    elif len(words) == 1:
        print("Done! Word is: ", words[0])
    else:
        print("No words left in the list!")
        break
        
    dayWord = input("Next word to try (or press enter to use suggestion): ").strip()
    if not dayWord and words:
        dayWord = best_word
        print("Using suggested word:", dayWord)