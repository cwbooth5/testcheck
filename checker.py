#!/usr/bin/env python

"""A test checker, for use prior to creating a review and checking in code."""

import argparse
import collections
import re
import subprocess
import sys


def words(text):
    """Return a list of all words in a given text."""
    return re.findall('[a-z]+', text.lower())


def train(features):
    """Return a dictionary of word occurrences."""
    model = collections.defaultdict(lambda: 1)
    for feature in features:
        model[feature] += 1
    return model


NWORDS = train(words(file('corpus.txt').read()))
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def edits1(word):
    """locate permutations"""
    s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in s if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in s for c in ALPHABET if b]
    inserts = [a + c + b for a, b in s for c in ALPHABET]
    return set(deletes + transposes + replaces + inserts)


def known_edits2(word):
    """known edits"""
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)


def known(words):
    """return a set of words from trained words"""
    return set(w for w in words if w in NWORDS)


def correct(word):
    """Find a corrected word."""
    candidates = known([word]) or known(edits1(word)) or \
        known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)


def add_term(term):
    """Add a term to the spellchecker text if it's not already there."""
    # See if we already added it.
    # Search in reverse
    with open('corpus.txt') as ofile:
        for line in reversed(ofile.readlines()):
            if ' ' + term + ' ' in line.strip():
                term = None
                break
    # Add it if we never encountered it.
    if term:
        with open('corpus.txt', 'a') as afile:
            afile.write(term)
            afile.write('\n')
        print "[ term '%s' added ]" % term


class CodeChecker(object):

    """This class allows a number of simple code quality checks for python.

    It's meant to be used prior to review and check in.

    NOTE: It can and should be influenced by coding styles of the dev group.
    That would mean a custom .pylintrc (for example) should probably be in
    place prior to running this so pylint has something to reference which
    specifies coding practices unique to this organization.
    """

    def __init__(self, inputfile, learning=False, verbose=False):
        """Take a single input file as a target for checks, all for learning.

        @param inputfile: The python file being checked
        @param learning: learning mode for the spell checker, defaults to False
        @param verbose: toggle verbose output
        """
        self.inputfile = inputfile
        self.learning = learning
        self.verbose = verbose

        self.pylint_score = None

    def check_spelling(self):
        """Execute the spell checker on the input file."""
        print '[ Spellcheck ]',
        # reference_lines = defaultdict(list)
        with open(self.inputfile) as cfile:
            data = cfile.readlines()
        for lineno, line in enumerate(data, start=1):
            for term in [x.lower() for x in line.split()]:
                if term.isalpha():
                    # reference_lines[lineno].append(term)
                    corrected = correct(term)
                    if term != corrected:
                        print "%d: Found '%s'; Corrected? '%s'" % (lineno,
                                                                   term,
                                                                   corrected)
                        if self.learning:
                            add_term(term)  # learning mode
        print '\t[DONE]'

    def complexity(self):
        """Calculate the complexity of the code"""
        print '[ Cyclomatic Complexity ]'
        print subprocess.check_output(['radon', 'cc', '-nae', self.inputfile])

    def metrics(self):
        """obtain raw metrics like line counts"""
        print '[ Raw Metrics ]'
        print subprocess.check_output(['radon', 'raw', self.inputfile])

    def pylint(self):
        """This runs pylint"""
        print '[ pylint ]',
        if self.verbose:
            subprocess.call(['pylint', '-r', 'n', self.inputfile])

        cmd = ['pylint', self.inputfile]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        score_output = proc.communicate()[0]
        for line in score_output.splitlines():
            if 'Your code has been rated' in line:
                score = line.strip()
                break
        self.pylint_score = score
        print self.pylint_score

    def run_everything(self):
        """Execute all available checks."""
        self.check_spelling()
        self.complexity()
        self.metrics()
        self.pylint()


def main(parser):
    """Provide an argument parser and take action"""
    inputs = parser.parse_args()
    verbosity = False or inputs.verbose
    learning = False or inputs.learning
    checkfile = inputs.filename
    checker = CodeChecker(checkfile, verbose=verbosity, learning=learning)
    if inputs.testall:
        checker.run_everything()
    if inputs.spell:
        checker.check_spelling()
    if inputs.complex:
        checker.complexity()
    if inputs.metrics:
        checker.metrics()
    if inputs.lint:
        checker.pylint()


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Python code checker thing')

    PARSER.add_argument('-a', action="store_true", dest="testall",
                        help="Run all tests")
    PARSER.add_argument('-s', action="store_true", dest="spell",
                        help="run spellcheck")
    PARSER.add_argument('-c', action="store_true", dest="complex",
                        help="run Cyclomatic Complexity check")
    PARSER.add_argument('-m', action="store_true", dest="metrics",
                        help="print raw metrics")
    PARSER.add_argument('-p', action="store_true", dest="lint",
                        help="run pylint and show score")
    PARSER.add_argument('-v', action="store_true", dest="verbose",
                        help="toggle verbose mode in pylint")
    PARSER.add_argument('-l', action="store_true", dest="learning",
                        help="toggle learning of new keywords (for spellcheck)")

    PARSER.add_argument('filename')

    sys.exit(main(parser=PARSER))

