import gzip 
import matplotlib.pyplot as plt
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="A program to sort the contents of 2 Sequence Read Files based on the index barcodes \n Fastq files must be zipped.")
    parser.add_argument("-r1", "--read_1_file", help="Directs to fastq for Read 1", type=str,required=True)
    parser.add_argument("-r2", "--index_1_file", help="Directs to fastq for Index 1", type=str,required=True)
    parser.add_argument("-r3", "--index_2_file", help="Directs to fastq for Index 2", type=str,required=True)
    parser.add_argument("-r4", "--read_2_file", help="Directs to fastq for Read 2", type=str,required=True)
    parser.add_argument("-I", "--Index_file", help="Gives text file containing barcodes.  Indexes are in 5th column", type=str,required=True)
    parser.add_argument("-c","--cutoff",help="Gives cutoff to define low quality base read.",type = int, required = False, default=20)
    parser.add_argument("-o", "--output", help="Gives directory to write output fastq and 2 plots", type=str,required=True)
    parser.add_argument("-hd","--ham_dist",help="Gives maximum hamming distance between two strings, as well as the maximum number of low quality reads.",type = int, required = False, default=0)
    return parser.parse_args()

args = get_args()
r1 = args.read_1_file
r2 = args.index_1_file
r3 = args.index_2_file   
r4 = args.read_2_file
index_file = args.Index_file
cutoff = args.cutoff
output_dir = args.output
hamming_dist = args.ham_dist


def rev_comp(seq: str)->str:
    '''This function returns the reverse complement of a given sequence string.'''
    rc = ''
    for i in range(len(seq)):
        if seq[-(i+1)].upper() == 'A':
            rc += 'T'
        elif seq[-(i+1)].upper() == 'T':
            rc += 'A'
        elif seq[-(i+1)].upper() == 'C':
            rc += 'G'
        elif seq[-(i+1)].upper() == 'G':
            rc += 'C'
        elif seq[-(i+1)].upper() == 'N':
            rc += 'N'
        else:
            return False
    return rc

def high_qual_read(qual_string: str,qual_cutoff: int,hamming_dist: int)->bool:
    '''This function returns True if all quality scores are >= given quality cutoff and False is any are < 20.'''
    low_qual = 0
    for i in qual_string:
        
        if ord(i) - 33 < qual_cutoff:
            low_qual += 1
            if low_qual > hamming_dist:
                return False
    return True

def hamming_distance(str1: str,str2: str)->int:
    '''For 2 given strings, this returns the number of mismatches in the strings (hamming distance) and the number of n's in the strings'''
    dist = 0
    if len(str1) != len(str2):
        return len(str1)

    for i in range(len(str1)):
        if str1[i] != str2[i] or str1[i].upper() == 'N' or str2[i].upper() == 'N':
            dist += 1

    return dist

def fastq_4_line_read(file_handle: str)->dict:
    ''' For a given file header, return the four lines of a fastq read and return a dictionary where each entry is one of the lines '''

    fastq_read = {}

    fastq_read['header'] = (file_handle.readline()).strip('\n')
    fastq_read['seq'] = (file_handle.readline()).strip('\n')
    fastq_read['line3'] = (file_handle.readline()).strip('\n')
    fastq_read['qual_score'] = (file_handle.readline()).strip('\n')

    return fastq_read

def create_files(index_file: str)->[set,dict]:
    '''This function will read all the indexes from the given file, return a list with each of the indexes, and open files to write with 
    the fileheaders in a dictionary for each read/index combo as well as r1 and r2 hopped and unknown'''

    with open(index_file,'r') as fh:
        indexes = set() #set to hold each of the indexes
        index_list = set() #set to hold each of the filenames 

        for line in fh:
            line = line.strip('\n')
            index = line.split()[4]
            indexes.add(index)
            index_list.add(f'r1_{index}.fastq')
            index_list.add(f'r2_{index}.fastq')

    index_list.add('r1_hopped.fastq')
    index_list.add('r2_hopped.fastq')
    index_list.add('r1_unknown.fastq')
    index_list.add('r2_unknown.fastq')

    file_names = {}
    for filename in index_list:
        file_names[filename] = [open(f'{output_dir}/{filename}', mode = 'w'),0]  #The second element of the list will increment each time that filename is used.

    return indexes,file_names

def write_to_file(read_dict: dict,output_file: str,index_dict: dict)->dict:
    '''Function to write contents of dictionary to a the given fastq file.
    read_dict will have one key for the header, the sequence, the "+", and the quality scores.
    The index_dict will have keys that are the output filenames with values as opened file objects to write to.'''

    header = read_dict['header']
    seq = read_dict['seq']
    qual_score = read_dict['qual_score']

    #Writes the new fastq to a new file.
    index_dict[output_file][0].write(f'{header}\n{seq}\n+\n{qual_score}\n')

    #Counts the number of records written to each file.
    index_dict[output_file][1]+= 1 

    return index_dict


index_set, file_dict = create_files(index_file)
hopped_record = {}


with gzip.open(r1,mode = 'rt') as read1, gzip.open(r2,mode = 'rt') as index1, gzip.open(r3,mode ='rt') as index2, gzip.open(r4,mode ='rt') as read2:
    while True:

        #Stores the 4 lines for a record in separate dictionaries for each input file.
        read_1_read = fastq_4_line_read(read1)
        index_1_read = fastq_4_line_read(index1)
        index_2_read = fastq_4_line_read(index2)
        read_2_read = fastq_4_line_read(read2)

        #Exit statement for the loop.  The barcode will only be empty at the end of the file.


        #Pull out sequences and qualities from index files
        index_1_bc = index_1_read['seq']
        index_1_qual = index_1_read['qual_score']
        index_2_bc = rev_comp(index_2_read['seq'])
        index_2_qual = index_2_read['qual_score']

        if index_1_bc == '':
            break

        old_read_1_header = read_1_read['header']
        old_read_2_header = read_2_read['header']

        read_1_read['header'] = f'{old_read_1_header}_{index_1_bc}-{index_2_bc}'
        read_2_read['header'] = f'{old_read_2_header}_{index_1_bc}-{index_2_bc}'


        if index_1_bc in index_set and index_2_bc in index_set:
            if high_qual_read(index_1_qual,cutoff,hamming_dist) and high_qual_read(index_2_qual,cutoff,hamming_dist):
                if hamming_distance(index_1_bc,index_2_bc) <= hamming_dist:
                    #These are the correctly paired reads
                    write_to_file(read_1_read,f'r1_{index_1_bc}.fastq',file_dict)
                    write_to_file(read_2_read,f'r2_{index_2_bc}.fastq',file_dict)

                else:
                    #These are index hopped

                    write_to_file(read_1_read,'r1_hopped.fastq',file_dict)
                    write_to_file(read_2_read,'r2_hopped.fastq',file_dict)

                    hopped = f'{index_1_bc}-{index_2_bc}'

                    if hopped in hopped_record:
                        hopped_record[hopped] += 1
                    else:
                        hopped_record[hopped] = 1

        #These are low quality or unknown barcodes
            else: 
                write_to_file(read_1_read,'r1_unknown.fastq',file_dict)
                write_to_file(read_2_read,'r2_unknown.fastq',file_dict)
        else:
            write_to_file(read_1_read,'r1_unknown.fastq',file_dict)
            write_to_file(read_2_read,'r2_unknown.fastq',file_dict)



freqs = [i[1] for i in file_dict.values()]


'''
These were plotting functions used in the first iteration of my code, but have since been replaced with a separate script.
'''

# plt.figure(1)
# plt.bar(file_dict.keys(),freqs)
# plt.xlabel('File Name')
# plt.ylabel('Number of Records per File')
# plt.title('Distribution of Records')
# labels = file_dict.keys()
# ax = plt.gca()
# ax.set_xticklabels(labels=labels,rotation=45)
# plt.tight_layout()
# plt.savefig(f'{output_dir}/Output_distribution.png')


# plt.figure(2)
# plt.bar(hopped_record.keys(),hopped_record.values())
# plt.xlabel('Hopped Indexes')
# plt.ylabel('Number of Occurences')
# plt.title('Number of Instances for each Barcode Hopping')
# labels = hopped_record.keys()
# ax = plt.gca()
# ax.set_xticklabels(labels=labels,rotation=45)
# plt.tight_layout()
# plt.savefig(f'{output_dir}/Index_Hopping_Frequency')

with open(f'{output_dir}/results.txt','w') as fout:
    fout.write('Distribution of Records\n')
    for keys,values in file_dict.items():
        fout.write(f'{keys}\t\t{values[1]}\n')
    
    fout.write('\nNumber of Instances for Each Barcode Hopping\n')
    for keys,values in hopped_record.items():
        fout.write(f'{keys}\t\t{values}\n')