#!/bin/bash
#SBATCH --partition=bgmp     ### queue to submit to
#SBATCH --job-name=demux     ### job name
#SBATCH --output=demux%j.out   ### file in which to store job stdout
#SBATCH --error=demux%j.err    ### file in which to store job stderr
#SBATCH --nodes=1              ### number of nodes to request
#SBATCH --cpus-per-task=20
#SBATCH -A bgmp                ### account

conda activate bgmp_py310

data_dir='/projects/bgmp/shared/2017_sequencing'
output_dir='/projects/bgmp/skupp/bioinfo/Bi622/Demultiplex/Assignment-the-third/real_output'

/usr/bin/time -v \
python demux.py -r1 ${data_dir}/1294_S1_L008_R1_001.fastq.gz -r2 ${data_dir}/1294_S1_L008_R2_001.fastq.gz \
-r3 ${data_dir}/1294_S1_L008_R3_001.fastq.gz -r4 ${data_dir}/1294_S1_L008_R4_001.fastq.gz \
-I ${data_dir}/indexes.txt -c 20 -o $output_dir -hd 2

pigz $output_dir/*.fastq
