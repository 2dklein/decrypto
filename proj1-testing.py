import numpy as np
import random as rn
import copy

# Grab npz file and clean it up for analysis
data = np.load('wp.npz')  # Load file
text = data['text']  # Access text
stext = str(text)  # Make the text string searchable
stext = stext.replace('- ', '')  # Clean up hyphened words

albet = "abcdefghijklmnopqrstuvwxyz"  # Alphabet string
coded = "zywdynfzmbboanxjrxiaimbbxpgaxwiyrymbpgoyxal"  # Given encrypted string
goal = "jackandjillwentupthehilltofetchapailofwater"
# Create random key dictionary
keys = []
for i in range(26):
    keys.append(albet[i])  # Create a list of letters
vals = np.copy(keys)  # Make a keys copy
rn.shuffle(vals)  # Shuffle values
zipper = zip(vals, keys)  # Create tuple list
master = dict(zipper)  # Convert tuple list to dict

# Create an alphabetical index (aldex)
numbers = range(26)
aldex = dict(zip(keys, numbers))  # aldex is letters : numbers
numdex = dict(zip(numbers, keys))  # numdex is numbers : letters

# Probability matrix creation
probmat = np.zeros((26, 26))
probtot = 0
for first in range(26):
    for second in range(26):
        # Count the pairs of letters in first-second order, assign them to probmat
        probmat[first, second] = stext.count(albet[first] + albet[second])
        probtot += probmat[first, second]  # Added a total probability for the matrix
# Normalize probmat
probmat = probmat / probtot
# Probmat now contains the normalized probability of two letters appearing next to each other.

# Translate the coded message using the initial random key
decode = ""
for ii in range(len(coded)):
    decode += master[coded[ii]]
print decode

# Assign a decode with probmat
numcode = []
for ii in range(len(decode)):
    numcode.append(aldex[decode[ii]])  # Convert the decoded message
print numcode  # Numcode is the decoded message in an alphabetical index list

# Idea 1: Sum probabilities
# Using the RNG keys dict, calculate the sum of the probabilities of letter pairs found.
probsum = 0.
for i in range(len(numcode) - 1):  # -1 for end of phrase
    probsum += probmat[numcode[i], numcode[i + 1]]  # Return prob of this letter pair
# print probsum  # Print the current probability sum that this is correct.


# Idea 2b: Exponential Annealing
Tmax = 1.
Tmin = 1e-4
# 0.436163462326 1e-9 0%
# 0.437289048081 1e-6 0%
# 0.430396107468 1e-4 0%
tau = 1e4

t_0 = 0

T = 100000
newkey = copy.deepcopy(master)
count = 0
while T > 0:
    # Swap two keys
    testkey = copy.deepcopy(newkey)
    aa, bb = numdex[rn.randrange(26)], numdex[rn.randrange(26)]  # Choose two random letters
    # print aa, bb
    testkey[aa], testkey[bb] = newkey[bb], newkey[aa]  # Find dict mappings and swap in testkey

    # Translate the coded message using the newkey
    decode = ""
    for ii in range(len(coded)):
        decode += testkey[coded[ii]]
    numcode = []  # Fresh numcode
    for ii in range(len(decode)):
        numcode.append(aldex[decode[ii]])  # Convert the decoded message
    # print numcode  # Numcode is the decoded message in an alphabetical index list

    # Rerun probsum
    testsum = 0.
    for i in range(len(numcode) - 1):  # -1 for end of phrase
        testsum += probmat[numcode[i], numcode[i + 1]]  # Return prob of this letter pair

    # Compare testsum to probsum and keep or reject
    if testsum > probsum:
        probsum = testsum
        newkey = copy.deepcopy(testkey)  # Keep, it's good
        count = 0
    # else:
    #     # Annealing
    #     if T > rn.randrange(1e6):  # Linear annealing
    #         probsum = testsum
    #         newkey = copy.deepcopy(testkey)
    #         print probsum  # Output a wrong but kept value
    #     # Loop
    if testsum < probsum:
        count += 1
        if count == 1000:
            probsum = testsum
            newkey = copy.deepcopy(testkey)
            count = 0
            print "."
    T -= 1  # Remove an annealing point

print probsum
print decode

success = 0
for i in range(len(coded)):
    if decode[i] == goal[i]:
        success += 1
print "Percent correct:", success/len(coded)
