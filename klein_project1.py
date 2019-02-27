import numpy as np
import random as rn
import copy
from string import ascii_lowercase as albet
import matplotlib.pyplot as plt


def load_source():
    # Grab npz file and convert to searchable string
    data = np.load('wp.npz')  # Load file
    text = str(data['text'])  # Access text and make the text string searchable
    return text


def decode(key):  # Convert code with passed key and return
    encrypted = "hjsdmgjdzlfxmztzfozldmlvjjsdhluazdmydjsvauhjduajfuaqmgjfuqfzfulfzpfluqjfgjfgzqtzxqfiqyzduolfxxzxqgluzxujuazndjnjmquqjfualuliikzfldzgdzluzxzwsli"
    msg = ""
    for ii in range(len(encrypted)):
        msg += key[encrypted[ii]]
    return msg


stext = load_source()  # Create source text

# Clean up text: hyphened words and roman numeral chapter numbers
stext = stext.replace('- ', '').replace('xxx', '').replace('xx', '').replace('iii', '').replace('ii', '').replace('xv', '')  # Clean up words

code = "hjsdmgjdzlfxmztzfozldmlvjjsdhluazdmydjsvauhjduajfuaqmgjfuqfzfulfzpfluqjfgjfgzqtzxqfiqyzduolfxxzxqgluzxujuazndjnjmquqjfualuliikzfldzgdzluzxzwsli"
goal = "fourscoreandsevenyearsagoourfathersbroughtforthonthiscontinentanewnationconceivedinlibertyanddedicatedtothepropositionthatallmenarecreatedequal"

# Create an alphabetical index (aldex)
aldex = {x: i for i, x in enumerate(albet)}  # dictionary converting letters to numbers for indexing probmat

# Probability matrix creation
probmat = np.zeros((26, 26))  # Initialize empty array
probtot = 0.
for first in range(26):
    for second in range(26):
        # Count the pairs of letters in first-second order, assign them to probmat
        probmat[first, second] = (np.log10(stext.count(albet[first] + albet[second]) + 1.)) + 1.

# For loop multiple test runs
correct, probs, swaps, maxs, tries_all = [], [], [], [], []  # Data collection lists
for j in range(50):
    tries = []  # Record probabilities tried, new for each run
    # Create random key dictionary
    keys = []
    for i in range(26):
        keys.append(albet[i])  # Create a list of letters
    vals = np.copy(keys)  # Make a keys copy
    rn.shuffle(vals)  # Shuffle values
    master = dict(zip(vals, keys))  # Convert lists to initial key, letters : letters

    # Translate the coded message using the initial random key
    initial = decode(master)

    # Using the RNG keys dict, calculate the sum of the probabilities of letter pairs found.
    probsum = 1.
    for i in range(len(initial) - 1):  # -1 for end of phrase
        probsum *= probmat[aldex[initial[i]], aldex[initial[i + 1]]]  # Return prob of this letter pair

    oldkey = copy.deepcopy(master)
    abs_max = 0.
    tau, T = 1000., 1000.
    swap = 0
    while T < 75000:
        eng = np.exp(- (2 * T / tau))

        # Swap two keys
        testkey = copy.deepcopy(oldkey)
        key1, key2 = rn.sample(list(testkey), 2)
        testkey[key1], testkey[key2] = testkey[key2], testkey[key1]
        test = decode(testkey)  # Decode encrypted text with this new key

        # Rerun probsum
        testsum = 1.
        for i in range(len(test) - 1):  # -1 for end of phrase
            testsum *= probmat[aldex[test[i]], aldex[test[i + 1]]]  # Return prob of this letter pair

        rng = rn.random()

        # Compare testsum to probsum and keep if higher
        if testsum > probsum:  # Keep better values
            probsum = testsum
            oldkey = copy.deepcopy(testkey)  # Keep, it's good
            swap += 1  # Count how many times a value is kept

        elif rng < eng:  # Scaling Annealing for wrong values
            probsum = testsum
            oldkey = copy.deepcopy(testkey)  # Keep
            swap += 1  # Count how many times a value is kept

        tries.append(probsum)
        # Loop
        T += 1

    # Statistics
    probs.append(probsum)  #
    last = decode(oldkey)
    print "Final key", j, ":", last
    swaps.append(swap)

    success = 0.
    for i in range(len(last)):
        if last[i] == goal[i]:
            success += 1.
    correct.append(success / len(goal))
    tries_all.append(tries)

print "\nStats:"
print "Number of runs:", len(correct)
print "Number of zero correct runs:", correct.count(0.0)
print "Average correct:", np.mean(correct)
print "Average accepted swaps:", np.mean(swaps)
print "Number of iterations", len(tries_all[0])

plt.figure(1)
plt.title("Chain Probability Over Time")
for i in range(len(tries_all)):
    plt.plot(tries_all[i])
plt.xlabel("Iteration")
plt.ylabel("Probability Correct")

plt.figure(2)
plt.title("Baseline")
plt.xlabel("Percent Correct")
plt.ylabel("Counts")
plt.hist(correct)
plt.show()
