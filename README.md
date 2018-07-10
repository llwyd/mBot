# markovMagpie
A terrible markov chain engine for generating tweets

## How it works

### Data Harvesting

* Assuming a sentence has n words.

* Two Arrays (Dictionaries)

  1. Contains `word[0]` with all possible `word[1]`.
  2. Contains `word[1:n]` with all possible `word[x+1]`.

* Python allows arrays within arrays

  - `{'Word[0]': ['Word[1]', 'Word[1]', 'Word[1]']}`
  - `{'Word[x]': ['Word[x+1]', 'Word[x+1]']}`
    - Array can be accessed recursively

### Generating Tweets

1. Randomly select `word[0]`.

  - Known as the ‘key’
  - Key is chosen at random to start the chain

2. Randomly select `word[1]` based on `word[0]`.

3. Randomly select `word[x]` until:

  - `word[x]` has no `word[x+1]`.
    - Typically a word with a full stop.

## Further Reading/References
