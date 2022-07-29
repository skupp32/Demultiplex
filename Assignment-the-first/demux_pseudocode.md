Problem:
When indexing sequences to do multiplex reads, barcodes are mixed between the different strands to be sequenced.  Because of this, the fastq files need to be filtered to include only one sequence.  The goal of this code is to separate each sequence into its own fastq.  Sequences with mismatching indices will be put into their own file, as will sequences with non-existent indices.


import necessary python libraries


def phred_score(q_score_string):
    '''Calculate the phred+33 score of every base for a given string.  If one base is too low quality, Q < 20,  put the read in unmatched.'''
    loop over every character in a string and calculate the phred+33 score.

    Test:
    input: "IIEIABCD"
    output: True

    input: "/ACDBIII"
    output: False

    input:
    return True if all bases above cutoff, false is at least one is below.

def rev_comp(seq):
    '''Computes and returns the reverse complement of a given sequence'''
    loop over every character in reverse in a sequence and store in a new string.

    Test:
    input: "ACGT"
    output: "ACGT"

    return the new string

open indexes.txt
store each of these indexes in a dictionary with values initialized to 0

open the 4 fastq files and the 52 output files
    if the sequence from index 1 matches the reverse complement of the sequence from index 2 and both are high enough quality (and no 'N')
        write each of the fastq records to the corresponding read and index file.  Update the header line to include the two indexes.  Increment the 1st entry in the dictionary with key equal to this barcode
    else if the two indexes do not match, but exist and are high quality
        write each of the fastq records to the corresponding read and index hopped fastq file. Update the header line to include the two indexes.  Increment the number of hopped reads.
    else if the indexes do not exist or are low quality
        write each of the fastq records to the corresponding read and unknown fastq file. Update the header line to include the two indexes.  Increment the number of unknown reads

Plot the distribution of properly matched indexes. 

This code will output the 52 FASTQ files as well as a plot with the distribution of matched indexes.