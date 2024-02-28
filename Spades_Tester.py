import Bio
import os
import glob
from Bio import Entrez
from Bio import SeqIO
log=open('PipelineProject.log', 'w')
inpath = '/home/vtrivedi1/Python-Pipeline-Vir-Trivedi/SRX*.fastq'
prepath = '/home/vtrivedi1/Python-Pipeline-Vir-Trivedi/'
fastqs = glob.glob(inpath)
#x is a list of all fastq paths from the directory being used
fastq_labels=[]
for path in fastqs:
    fastq_labels.append(path[-18:-8])
fastq_labels=set(fastq_labels)
fastq_donor_dict = {}
for label in fastq_labels:
    if label == 'SRX2896375':
        fastq_donor_dict[label]='Donor 3 (6dpi)'
    elif label == 'SRX2896363':
        fastq_donor_dict[label]='Donor 1 (6dpi)'
    elif label == 'SRX2896360':
        fastq_donor_dict[label]='Donor 1 (2dpi)'
    elif label == 'SRX2896374':
        fastq_donor_dict[label]='Donor 3 (2dpi)'
#Work through writing to log file logic?
mapped = glob.glob('/home/vtrivedi1/Python-Pipeline-Vir-Trivedi/SRX*_mapped*.fq.gz')
total_reads=list(mapped+fastqs)
for label in fastq_labels:
    precount_1=0
    precount_2=0
    count_1=0
    count_2=0
    for file in total_reads:
        if file == f'/home/vtrivedi1/Python-Pipeline-Vir-Trivedi/{label}_1.fastq':
            '''
            with open(str(file), 'r') as handle:
                for record in SeqIO.parse(handle, 'fastq'):
                    precount_1 += 1
            '''
        if file == f'/home/vtrivedi1/Python-Pipeline-Vir-Trivedi/{label}_2.fastq':
            '''
            with open(str(file), 'r') as handle:
                for record in SeqIO.parse(handle, 'fastq'):
                    precount_2 += 1
            '''
        if file == f'/home/vtrivedi1/Python-Pipeline-Vir-Trivedi/{label}_mapped_1.fq.gz':
            '''
            with open(str(file), 'r') as handle:
                for record in SeqIO.parse(handle, 'fastq'):
                    count_1 += 1
            '''
        if file == f'/home/vtrivedi1/Python-Pipeline-Vir-Trivedi/{label}_mapped_2.fq.gz':
            '''
            with open(str(file), 'r') as handle:
                for record in SeqIO.parse(handle, 'fastq'):
                    count_2 += 1
            '''
    #print(f'{fastq_donor_dict[label]} had {precount_1 + precount_2} reads before Bowtie2 filtering and {count_1 + count_2} read pairs after.')
    #ASK ABOUT IN LAB/CLASS
'''
with open(fastq_file, "r") as handle:
        for record in SeqIO.parse(handle, "fastq"):
            count += 1
    return count
'''
os.system('spades.py --only-assembler --pe1-1 SRX2896360_mapped_1.fq.gz --pe1-2 SRX2896360_mapped_2.fq.gz --pe2-1 SRX2896363_mapped_1.fq.gz --pe2-2 SRX2896363_mapped_2.fq.gz --pe3-1 SRX2896374_mapped_1.fq.gz --pe3-2 SRX2896374_mapped_2.fq.gz --pe4-1 SRX2896375_mapped_1.fq.gz --pe4-2 SRX2896375_mapped_2.fq.gz -o PipelineProject_Vir_Trivedi/')
