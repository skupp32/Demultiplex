#!/bin/bash
#SBATCH --partition=bgmp     ### queue to submit to
#SBATCH --job-name=base_q_score%j     ### job name
#SBATCH --output=base_q_score.out    ### file in which to store job stdout
#SBATCH --error=base_q_score.err     ### file in which to store job stderr
#SBATCH --nodes=1               ### number of nodes to request
#SBATCH -A bgmp                ### account

conda activate bgmp_py310

/usr/bin/time -v \
python demux_base_exp.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz -l 101
python demux_base_exp.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz -l 8
python demux_base_exp.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz -l 101

#python demux_base_exp.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz -l 8

python demux_base_exp.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz -l 101
python demux_base_exp.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz -l 8
python demux_base_exp.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz -l 101
