	NEPALI TEXT TOKENIZER
A text tokenizer that splits, stops, and stems exclusive Nepali text, optimized grammatically for the Nepali language
Stopwords are the high occurrence words that do not provide information on the relevance of any given word, and hence
are not considered when making tokens. The stopword list provides those words for the Nepali language.
SAMPLE TEXT LINK: https://www.samakalinsahitya.com/sahitya/details/7325 COURTESEY OF DR. GOMA DEVI SHARMA ADHIKARI

Examples of stopwords in Nepali language: र, ल, पो, छ

The most popular stems are also removed, creating uniform words from different cases

Examples: हरू, मा, ले, and any combination of the aformentioned (Nepali uses conjugations to show different verb forms, and hence many
suffixes can be added on top of another)

The input text to this program is in gzip format, while the output is in three files:

1. output_token_list.txt shows every original word in the text, and next to it is the stopped and stemmed form of the word
2. output_statistics.txt shows the most common tokens, in descending order
3. output_heap.txt shows the occurence of words to the occurence of unique words in the text, the left column is every 10 words found, while
the right column shows how many unique words have been found until that point
