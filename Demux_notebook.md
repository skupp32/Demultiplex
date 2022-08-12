# July 26th, 2022

Fastq files in /projects/bgmp/shared/2017_sequencing
Git Repo: /projects/bgmp/skupp/bioinfo/Bi622/Demultiplex

To find number of reads in each fastq:

```
zcat 1294_S1_L008_R1_001.fastq.gz | wc -l
1452986940
zcat 1294_S1_L008_R2_001.fastq.gz | wc -l
1452986940
zcat 1294_S1_L008_R3_001.fastq.gz | wc -l
1452986940
zcat 1294_S1_L008_R4_001.fastq.gz | wc -l
1452986940
```

and divided by 4.

To find the length of each sequence:

```
zcat 1294_S1_L008_R1_001.fastq.gz | head -2 |tail -1| wc
      1       1     102
zcat 1294_S1_L008_R2_001.fastq.gz | head -2 |tail -1| wc
      1       1       9
zcat 1294_S1_L008_R3_001.fastq.gz | head -2 |tail -1| wc
      1       1       9
zcat 1294_S1_L008_R4_001.fastq.gz | head -2 |tail -1| wc
      1       1     102
```

To determine Phred Encoding:

```
zcat 1294_S1_L008_R4_001.fastq.gz | head -4 |tail -1
#AAFAFJJ-----F---7-<FA-F<AFFA-JJJ77<FJFJFJJJJJJJJJJAFJFFAJJJJJJJJFJF7-AFFJJ7F7JFJJFJ7FFF--A<A7<-A-7--
zcat 1294_S1_L008_R3_001.fastq.gz | head -4 |tail -1
#AAAAJJF
zcat 1294_S1_L008_R2_001.fastq.gz | head -4 |tail -1
#AA<FJJJ
zcat 1294_S1_L008_R1_001.fastq.gz | head -4 |tail -1
A#A-<FJJJ<JJJJJJJJJJJJJJJJJFJJJJFFJJFJJJAJJJJ-AJJJJJJJFFJJJJJJFFA-7<AJJJFFAJJJJJF<F--JJJJJJF-A-F7JJJJ
```

Because each of these had ascii scores corresponding with less than 64, it must be a Phred +33 encoding.


The sequences in `1294_S1_L008_R2_001.fastq.gz` correspond with the indexes found in `indexes.txt`.  The reverse complement of each of the indexes is in the corresponding read of `1294_S1_L008_R3_001.fastq.gz`

Created test file for demux_base_exp.py with
`zcat /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz | head -200 > unit_test.txt` then `zcat /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz | head -200000| tail -200 >> unit_test.txt`

Script seems to work on test file.  Will add argparse to accept filename and read lengths

running python on bgmp_py310

Number of 'N' in the index files:

```
zcat 1294_S1_L008_R2_001.fastq.gz | sed -n '2~4p'| grep -c "N"
3976613
zcat 1294_S1_L008_R3_001.fastq.gz | sed -n '2~4p'| grep -c "N"
3328051
```

# July 27, 2022
Runs did not work. Gave argparse an absolute path with '/' in it so it could not create the figures with that name.  Changed it and running on index 1.

Created one line command to cound number of 'N' in both the index files.

```
for file in `ls *R[2,3]*`; do echo $file; zcat $file| sed -n '2~4p' | grep -c "N"; done
1294_S1_L008_R2_001.fastq.gz
3976613
1294_S1_L008_R3_001.fastq.gz
3328051
```

Running python script again.  Working on pseudocode.

# July 28, 2022
Writing unit tests for demux algorithm-

Unit Tests:
4 input fastq files.  are called `r<read num>_unit_test.fastq` and are in Assignment_the_first directory.
1 seq will properly match.  
1 will be hopped.
1 will fail because of unknown index, 1 will fail because of low quality, and 1 because of an N in the index.
Will output 2 matched files, 2 hopped, and 2 unknown (1 for each read)

Expected Output Files:
r1_AA.fastq- 4 lines 1 read
r2_AA.fastq- 4 lines 1 read
r1_hopped.fastq- 4 lines 1 read
r2_hopped.fastq- 4 lines 1 read
r1_unknown.fastq- 12 lines 3 reads
r2_unknown.fastq- 12 lines 3 reads

July 29, 2022
Good cutoff score could be Q = 20 because the odds of misidentifying an index is low, but it still keeps much of the data.
Finishing function defs in pseudocode and pushing to GitHub.

# August 2, 2022
Writing code to demultiplex fastq files.  Called `demux.py` in `/projects/bgmp/skupp/bioinfo/Bi622/Demultiplexing/Assignment-the-third`
Functions all appear to work independently.  Need to write loop to read in every record, sort, and write to files.

Make sure to run in conda env bgmp_py310

For some reason some of the f-strings with dictionary names not working.

Running test files with:
```
python demux.py -r1 $dir/r1_unit_test.fastq.gz -r2 $dir/r2_unit_test.fastq.gz -r3 $dir/r3_unit_test.fastq.gz -r4 $dir/r4_unit_test.fastq.gz -I indexes.txt -o $dir/output -c 20
```

# Auguest 3, 2022
Running on slurm.  No errors so far.  There were too few files need to check what's going on.  My Histogram labels are also unreadable.  Need to re-run.  Also write code to produce an output results file.

# August 8, 2022
demux not correctly sorting files.  Need to check logic.  Also adding argparse statement to allow user to control the hamming distance between strings and the number of low quality reads.
New command to run test files:
```
dir=/projects/bgmp/skupp/bioinfo/Bi622/Demultiplex/Assignment-the-third
python demux.py -r1 $dir/r1_unit_test.fastq.gz -r2 $dir/r2_unit_test.fastq.gz -r3 $dir/r3_unit_test.fastq.gz -r4 $dir/r4_unit_test.fastq.gz -I indexes.txt -o $dir/output -c 20 -hd 0
```
Everything works for unit test now.  Issue was with test index file.  Re-running on whole data set.

After running, there are now 2905973880 total lines in all of the files.  Need to compare with someone else.
The plots still are difficult to make legible.  May need something like a heat map to properly display the data for index hopping.

Output from /usr/bin/time -v for demux script:

```
Command being timed: "python demux.py -r1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz -r2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz -r3 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz -r4 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz -I /projects/bgmp/shared/2017_sequencing/indexes.txt -c 20 -o /projects/bgmp/skupp/bioinfo/Bi622/Demultiplex/Assignment-the-third/real_output -hd 2"
        User time (seconds): 4494.23
        System time (seconds): 117.40
        Percent of CPU this job got: 93%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 1:21:59
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 296156
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 0
        Minor (reclaiming a frame) page faults: 2386795
        Voluntary context switches: 50211
        Involuntary context switches: 311668
        Swaps: 0
        File system inputs: 0
        File system outputs: 0
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 0

```

# August 9, 2022
Creating script to plot data from results output file.  Struggling to use heatmaps.  Trying 3d barplot


# August 11, 2022
Using heatmap, plotted log10 of all number of index pairs to better display smaller data.
The percentage of reads in each file is:

```
hopped: 0.16%
TGTTCCGT: 4.24%
GATCTTGC: 0.98%
GATCAAGG: 1.77%
TCTTCGAC: 11.31%
ATCGTGGT: 1.85%
CGATCGAT: 1.51%
TCGACAAG: 1.03%
unknown: 11.14%
TCGAGAGT: 3.13%
GCTACTCT: 1.96%
TAGCCATG: 2.85%
ATCATGCG: 2.69%
TATGGCAC: 2.98%
AGAGTCCA: 3.02%
AGGATAGC: 2.33%
ACGATCAG: 2.14%
CACTTCAC: 1.12%
TACCGGAT: 20.34%
TCGGATTC: 1.23%
CGGTAATC: 1.33%
CTAGCTCA: 4.65%
CTCTGGAT: 9.34%
AACAGCGA: 2.37%
GTCCTAAG: 2.36%
GTAGCGTA: 2.17%
```
Plotting each type of file (unknown, hopped, and correctly matched for each index.)  Then pushing to GitHub.