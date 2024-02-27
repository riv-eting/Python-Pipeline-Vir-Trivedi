import Bio
import os
import glob
from Bio import Entrez
inpath = '/home/vtrivedi1/Python-Pipeline-Vir-Trivedi/SRX*.fastq'
fastqs = glob.glob(inpath)
#x is a list of all fastq paths from the directory being used
print(fastqs)
fastq_labels=[]
for path in fastqs:
    fastq_labels.append(path[-18:-8])
fastq_labels=set(fastq_labels)
print(fastq_labels)
'spades.py -k 77,99,127 -t 2 --only-assembler -1 SRR5364281_1.fastq -2 SRR5364281_2.fastq -o SRR5364281_assembly/'
