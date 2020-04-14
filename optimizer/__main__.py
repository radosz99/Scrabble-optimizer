import anagram as angrm

if __name__ == '__main__':
    # Get the letters from the command line and return all anagrams.
    letters="zwieźć"
    


    for word in angrm.anagram(letters, "words.txt"):
        print(word)