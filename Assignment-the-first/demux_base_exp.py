import argparse
import numpy as np
import matplotlib.pyplot as plt
import gzip

def get_args():
    parser = argparse.ArgumentParser(description="A program to plot the average score at each sequence position of a fastq file.")
    parser.add_argument("-f", "--file_name", help="Gives fastq to examine", type=str,required=True )
    parser.add_argument("-l","--length",help = "Tells the program the length of each read.  Assumes the same for each.",type = int, required = True)
    return parser.parse_args()

def convert_phred(letter: str) -> int:
    """Converts a single character into a phred score"""
    score = ord(letter) - 33
    return score


args = get_args()
file = args.file_name
length = args.length

score_array = np.zeros(length)

with gzip.open(file,mode = 'rt') as fq:
    line_num = 0
    for line in fq:
        line = line.strip('\n')
        line_num += 1
        if line_num % 4 == 0:
            for bp_pos,qual in enumerate(line):
                new_score = convert_phred(qual)
                score_array[bp_pos] += new_score

score_array = [i/line_num*4 for i in score_array]
file = file.split('/')
file = file[len(file)-1]
img_name = f'{file[0:-9]}_mean_qual.png'



plt.bar(range(len(score_array)),score_array)
plt.xlabel('Base Position')
plt.ylabel('Mean Quality Score')
plt.title('Mean Quality Score by Base Position')
plt.savefig(img_name,format = 'png')