# Assignment the First

## Part 1
1. Be sure to upload your Python script.

| File name | label | Read length | Phred encoding |
|---|---|---|---|
| 1294_S1_L008_R1_001.fastq.gz |  read 1| 101 | Phred +33 |
| 1294_S1_L008_R2_001.fastq.gz |  index 1| 8 | Phred +33 |
| 1294_S1_L008_R3_001.fastq.gz |  index 2| 8 | Phred +33 |
| 1294_S1_L008_R4_001.fastq.gz |  read 2| 101 | Phred +33 |

2. Per-base NT distribution

    1. 
    ![](https://github.com/skupp32/Demultiplex/blob/master/Assignment-the-first/1294_S1_L008_R1_001_mean_qual.png)
    ![](https://github.com/skupp32/Demultiplex/blob/master/Assignment-the-first/1294_S1_L008_R2_001_mean_qual.png)
    ![](https://github.com/skupp32/Demultiplex/blob/master/Assignment-the-first/1294_S1_L008_R3_001_mean_qual.png)
    ![](https://github.com/skupp32/Demultiplex/blob/master/Assignment-the-first/1294_S1_L008_R4_001_mean_qual.png)
    2. A quality score above 20 should be sufficient to ensure that mixed reads do not mix.  This corresponds to per base error rate of 0.01.  Assuming that the smallest hamming distance is 4, the probability of misassigning an index is ~6.7e-7.  This is calculated by the binomial distribution probability density function: $ _8c_4 * 0.99^4 * 0.01^4 $  
This would be expected to result in roughly 1 out of every 100,000 indexes being misidentified as another.
    3. 
        ```
        for file in `ls *R[2,3]*`; do echo $file; zcat $file| sed -n '2~4p' | grep -c "N"; done
        1294_S1_L008_R2_001.fastq.gz
        3976613
        1294_S1_L008_R3_001.fastq.gz
        3328051
        ```

## Part 2
1. Define the problem
2. Describe output
3. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [>=6 expected output FASTQ files](../TEST-output_FASTQ).
4. Pseudocode
5. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement

Problem:
When indexing sequences to do multiplex reads, barcodes are mixed between the different strands to be sequenced.  Because of this, the fastq files need to be filtered to include only one sequence.  The goal of this code is to separate each sequence into its own fastq.  Sequences with mismatching indices will be put into their own file, as will sequences with non-existent indices.

1.  Read in indexes.txt to store each of the index strings in a variable in the file.
2.  Read all 4 fastq files into python line-by-line.
3.  Check that for a corresponding set of reads that the index in each of the index reads matches.
    i.  If the indexes match, send the 4 fastq file lines for a read  to a file for that specific index and read.
    ii.  If the indexes do not match but are in the list of indexes, send them to  file for mismatching reads (one for each read)
    iii. If the indexes do not exist in the list or are too low quality, it will send them to a file for unknown indexes.


