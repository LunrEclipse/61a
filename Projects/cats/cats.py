"""Typing test implementation"""

from typing import SupportsBytes
from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns True. If there are fewer than K such paragraphs, return
    the empty string.

    Arguments:
        paragraphs: a list of strings
        select: a function that returns True for paragraphs that can be selected
        k: an integer

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> choose(ps, s, 0)
    'hi'
    >>> choose(ps, s, 1)
    'fine'
    >>> choose(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    res = ''
    count = 0 
    for x in range(len(paragraphs)):
        if(select(paragraphs[x])):
            if count == k:
                return paragraphs[x]
            else:
                count += 1
    return res
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether
    a paragraph contains one of the words in TOPIC.

    Arguments:
        topic: a list of words related to a subject

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def helper(paragraph):
        paragraph = paragraph.lower()
        paragraph = remove_punctuation(paragraph)
        paragraph = " " + paragraph + " "
        #print(paragraph)
        for x in range(len(topic)):
            temp = " " + topic[x].lower() + " "
            if temp in paragraph:
                return True
        return False
    return helper
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    Arguments:
        typed: a string that may contain typos
        reference: a string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    if(len(typed) == 0 and len(reference) != 0):
        return 0.0
    if(len(typed) != 0 and len(reference) == 0):
        return 0.0

    typedList = []
    referenceList = []
    
    hasSpace = False
    if " " in typed:
        hasSpace = True
    while(hasSpace):
        temp = typed.index(" ")
        typedList.append(typed[:temp])
        typed = typed[temp+1:]
        typed = typed.strip()
        if " " not in typed:
            hasSpace = False
    typedList.append(typed)

    hasSpace = False
    if " " in reference:
        hasSpace = True
    while(hasSpace):
        temp = reference.index(" ")
        referenceList.append(reference[:temp])
        reference = reference[temp+1:]
        reference = reference.strip()
        if " " not in reference:
            hasSpace = False
    referenceList.append(reference)

    #print(typedList)
    #print(referenceList)

    correct = 0
    for i in range(0, len(referenceList)):
        if i < len(typedList) and referenceList[i] == typedList[i]:
            correct += 1
    return correct / len(typedList) * 100
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.

    Arguments:
        typed: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    return (len(typed)/5) / (elapsed/60)
    # END PROBLEM 4


###########
# Phase 2 #
###########

def autocorrect(typed_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from TYPED_WORD. Instead returns TYPED_WORD if that difference is greater
    than LIMIT.

    Arguments:
        typed_word: a string representing a word that may contain typos
        valid_words: a list of strings representing valid words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    if typed_word in valid_words:
        return typed_word
    
    lowest = diff_function(typed_word, valid_words[0], limit)
    word = valid_words[0]
    for x in range(1, len(valid_words)):
        cur = diff_function(typed_word, valid_words[x], limit)
        if cur < lowest:
            lowest = cur
            word = valid_words[x]
    if(lowest > limit):
        return typed_word
    else:
        return word

    # END PROBLEM 5


def feline_flips(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths and returns the result.

    Arguments:
        start: a starting word
        goal: a string representing a desired goal word
        limit: a number representing an upper bound on the number of chars that must change

    >>> big_limit = 10
    >>> feline_flips("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> feline_flips("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> feline_flips("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> feline_flips("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> feline_flips("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    """
    # BEGIN PROBLEM 6
    if len(start) == 0 and len(goal) == 0:
        return 0
    if len(start) == 0 or len(goal) == 0:
        if limit == 0:
            return 1
        elif len(start) == 0:
            return 1 + feline_flips(start, goal[1:], limit-1)
        elif len(goal) == 0:
            return 1 + feline_flips(start[1:], goal, limit-1)
    else:
        if start[0] == goal[0]:
            return feline_flips(start[1:], goal[1:], limit)
        else:
            if limit == 0:
                return 1
            else:
                return 1 + feline_flips(start[1:], goal[1:], limit-1)
    # END PROBLEM 6


def minimum_mewtations(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL.
    This function takes in a string START, a string GOAL, and a number LIMIT.

    Arguments:
        start: a starting word
        goal: a goal word
        limit: a number representing an upper bound on the number of edits

    >>> big_limit = 10
    >>> minimum_mewtations("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    """

    #print(start == goal)
    if start == goal:  # Fill in the condition
        return 0

    elif limit == 0:  # Feel free to remove or add additional cases
        return 1
    

    # else:
    #     #print(start, goal)
    #     if(len(start) == len(goal)): #substitue
    #         x = 0
    #         while(start[x] == goal[x]):
    #             x += 1
    #         substitue = start[:x] + goal[x] + start[x+1:]
    #         add = start[:x] + goal[x] + start[x:]
    #         if(x == len(start)):
    #             remove = start[:len(start) - 1]
    #         else:
    #             remove = start[:x] + start[x+1:]

    #         return min((1 + minimum_mewtations(add, goal, limit-1)), (1 + minimum_mewtations(remove, goal, limit-1)), (1+minimum_mewtations(substitue, goal, limit-1)))
    #     elif(len(start) > len(goal)): #remove
    #         x = 0
    #         while(x < len(goal)-1 and start[x] == goal[x]):
    #             x += 1
    #         if(x == len(goal) -  1 and start[x+1] == goal[len(goal)-1]):
    #             remove = start[:x] + start[x+1:]
    #         elif(x == len(goal) - 1):
    #             remove = start[:len(start) - 1]
    #         else:
    #             remove = start[:x] + start[x+1:]
    #         return 1 + minimum_mewtations(remove, goal, limit-1)

    #     else: #add
    #         x = 0
    #         while(x < len(start)-1 and start[x] == goal[x]):
    #             x += 1
    #         add = start[:x] + goal[x] + start[x:]
    #         if len(add) == len(goal):
    #             backAdd = start + goal[len(start)]
    #             if(feline_flips(add, goal, limit) < feline_flips(backAdd, goal, limit)):
    #                 return 1 + minimum_mewtations(add, goal, limit-1)
    #             else:
    #                 return 1 + minimum_mewtations(backAdd, goal, limit-1)
    #         return 1 + minimum_mewtations(add, goal, limit-1)

    
    else:
        #print(start, goal)

        #remove
        # temp = start[:len(start)-1]
        # low = feline_flips(temp, goal, limit)
        # print(temp, low)
        # for x in range(0, len(start)-1):
        #     cur = start[:x] + start[x+1:]
        #     flips = feline_flips(cur, goal, limit)
        #     print(cur, flips)
        #     if(flips < low):
        #         temp = cur
        #         low = flips
        # remove = temp
        # removeFlips = low
        temp = start[1:]
        low = feline_flips(temp, goal, limit)
        for x in range(1, len(start)):
            cur = start[:x] + start[x+1:]
            flips = feline_flips(cur, goal, limit)
            if(flips < low):
                temp = cur
                low = flips
        remove = temp
        removeFlips = low          

        if(len(start) == len(goal)):
            #substitute
            x = 0
            while(start[x] == goal[x]):
                x += 1
            substitute = start[:x] + goal[x] + start[x+1:]
            subFlips = feline_flips(substitute, goal, limit)
            #add
            temp = start + goal[len(goal)-1]
            low = feline_flips(temp, goal, limit)
            for x in range(0, len(start)-1):
                cur = start[:x] + goal[x] + start[x:]
                flips = feline_flips(cur, goal, limit)
                if(flips < low):
                    temp = cur
                    low = flips
            add = temp
            addFlips = low
            
            #return min((1 + minimum_mewtations(add, goal, limit-1)), (1 + minimum_mewtations(remove, goal, limit-1)), (1+minimum_mewtations(substitute, goal, limit-1)))
            # print("Add:", add, addFlips)
            # print("Sub:", substitute, subFlips)
            # print("Remove:", remove, removeFlips)
            if(abs(addFlips-removeFlips) <= 1 and abs(addFlips-subFlips) <= 1):
                return min((1 + minimum_mewtations(add, goal, limit-1)), (1 + minimum_mewtations(remove, goal, limit-1)), (1+minimum_mewtations(substitute, goal, limit-1)))
            if(addFlips < subFlips and addFlips < removeFlips):
                if(abs(addFlips-removeFlips) <= 1):
                    return min((1 + minimum_mewtations(add, goal, limit-1)), (1 + minimum_mewtations(remove, goal, limit-1)))
                elif(abs(addFlips-subFlips) <= 1):
                    return min((1 + minimum_mewtations(add, goal, limit-1)), (1+minimum_mewtations(substitute, goal, limit-1)))
                else:
                    return 1 + minimum_mewtations(add, goal, limit-1)
            elif(removeFlips < addFlips and removeFlips < removeFlips):
                if(abs(removeFlips-addFlips) <= 1):
                    return min((1 + minimum_mewtations(remove, goal, limit-1)), (1 + minimum_mewtations(add, goal, limit-1)))
                elif(abs(removeFlips-subFlips) <= 1):
                    return min((1 + minimum_mewtations(remove, goal, limit-1)), (1 + minimum_mewtations(substitute, goal, limit-1)))
                else:
                    return 1 + minimum_mewtations(remove, goal, limit-1)
            else:
                if(abs(subFlips-removeFlips) <= 1):
                    return min((1 + minimum_mewtations(substitute, goal, limit-1)), (1 + minimum_mewtations(remove, goal, limit-1)))
                elif(abs(addFlips-addFlips) <= 1):
                    return min((1 + minimum_mewtations(substitute, goal, limit-1)), (1 + minimum_mewtations(add, goal, limit-1)))
                else:
                    return 1 + minimum_mewtations(substitute, goal, limit-1)
        elif(len(start) > len(goal)):         
            return 1 + minimum_mewtations(remove, goal, limit-1)
        else:
            #add
            temp = start + goal[len(goal)-1]
            low = feline_flips(temp, goal, limit)
            for x in range(0, len(goal)-1):
                cur = start[:x] + goal[x] + start[x:]
                flips = feline_flips(cur, goal, limit)
                if(flips < low):
                    temp = cur
                    low = flips
            add = temp
            return (1 + minimum_mewtations(add, goal, limit-1))

    




def final_diff(start, goal, limit):
    """A diff function that takes in a string START, a string GOAL, and a number LIMIT.
    If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function.'


FINAL_DIFF_LIMIT = 6  # REPLACE THIS WITH YOUR LIMIT


###########
# Phase 3 #
###########


def report_progress(sofar, prompt, user_id, upload):
    """Upload a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.

    Arguments:
        sofar: a list of the words input so far
        prompt: a list of the words in the typing prompt
        user_id: a number representing the id of the current user
        upload: a function used to upload progress to the multiplayer server

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> sofar = ['how', 'are', 'you']
    >>> prompt = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(sofar, prompt, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], prompt, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    # BEGIN PROBLEM 8
    count = 0
    for i in range(len(sofar)):
        if sofar[i] != prompt[i]:
            progress = count / len(prompt)
            upload({'id': user_id, 'progress': progress})
            return progress
        else:
            count += 1
    progress = count / len(prompt)
    upload({'id': user_id, 'progress': progress})
    return progress

    # END PROBLEM 8


def time_per_word(words, times_per_player):
    """Given timing data, return a match data abstraction, which contains a
    list of words and the amount of time each player took to type each word.

    Arguments:
        words: a list of words, in the order they are typed.
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> match = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> get_words(match)
    ['collar', 'plush', 'blush', 'repute']
    >>> get_times(match)
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    # BEGIN PROBLEM 9
    times = []
    for player in times_per_player:
        temp = []
        for i in range(len(player)-1):
            temp.append(abs(player[i] - player[i+1]))
        times.append(temp)
    return match(words, times)
    "*** YOUR CODE HERE ***"
    # END PROBLEM 9


def fastest_words(match):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        match: a match data abstraction as returned by time_per_word.

    >>> p0 = [5, 1, 3]
    >>> p1 = [4, 1, 6]
    >>> fastest_words(match(['Just', 'have', 'fun'], [p0, p1]))
    [['have', 'fun'], ['Just']]
    >>> p0  # input lists should not be mutated
    [5, 1, 3]
    >>> p1
    [4, 1, 6]
    """
    player_indices = range(len(get_times(match)))  # contains an *index* for each player
    word_indices = range(len(get_words(match)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    res = []
    for i in range(len(get_times(match))):
        res.append([])
    for i in range(len(get_times(match)[0])):
        min = get_times(match)[0][i]
        index = 0
        for j in range(1, len(get_times(match))):
            if get_times(match)[j][i] < min:
                min = get_times(match)[j][i]
                index = j
        res[index].append(get_words(match)[i])
    return res
        
            
    # END PROBLEM 10


def match(words, times):
    """A data abstraction containing all words typed and their times.

    Arguments:
        words: A list of strings, each string representing a word typed.
        times: A list of lists for how long it took for each player to type
            each word.
            times[i][j] = time it took for player i to type words[j].

    Example input:
        words: ['Hello', 'world']
        times: [[5, 1], [4, 2]]
    """
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(match, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(match[0]), "word_index out of range of words"
    return match[0][word_index]


def get_words(match):
    """A selector function for all the words in the match"""
    return match[0]


def get_times(match):
    """A selector function for all typing times for all players"""
    return match[1]


def time(match, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(match[0]), "word_index out of range of words"
    assert player_num < len(match[1]), "player_num out of range of players"
    return match[1][player_num][word_index]


def match_string(match):
    """A helper function that takes in a match object and returns a string representation of it"""
    return "match(%s, %s)" % (match[0], match[1])


enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
