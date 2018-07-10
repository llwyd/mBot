# markovMagpie
A terrible markov chain engine for generating tweets

## How it works

### Data Harvesting

* Assuming a sentence has n words.

* Two Arrays (Dictionaries)

  1. Contains `word[0]` with all possible `word[1]`.
  2. Contains `words[1:n]` with all possible `word[x+1]`.

* Python allows arrays within arrays

  - `{'Word[0]': ['Word[1]', 'Word[1]', 'Word[1]']}`
  - `{'Word[x]': ['Word[x+1]', 'Word[x+1]']}`
    - Array can be accessed recursively

### Generating Tweets

## Further Reading/References
