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