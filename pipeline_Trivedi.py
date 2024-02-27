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
#The above loop iterates over each of the file paths stored in fastqs and isolates their specific SRX identity sequences in a set
#This set will allow us to isolate paired fastq files and run them through bowtie
#Below, we enter the bowtie space :D
Entrez.email='vtrivedi1@luc.edu'
ID = 'NC_006273.2'
handle=Entrez.efetch(db='nucleotide',id=ID,rettype='fasta',retmode='text')
index_fasta = f'{ID}.fna'
with open(index_fasta, 'w') as w:
    w.write(handle.read())
os.system('bowtie2-build ' + index_fasta + ' HCMV')
#To get the fna file (NC_006273.2) for indexing, I used entrez efetch using the nucleotide database and the NC accession number
ones=[]
twos=[]
for path in fastqs:
    if path[-7]=='1':
        ones.append(path)
    if path[-7]=='2':
        twos.append(path)
for label in fastq_labels:
    for first in ones:
        if first[-18:-8] == f'{label}':
            a = first
    for second in twos:
        if second[-18:-8] == f'{label}':
            b = second
    print(a, b)
'''
for label in fastq_labels:
    for path in fastqs:
        if path[-18:-6] == f'{label}_1':
            ones.append(path)
for label in fastq_labels:
    for path in fastqs:
        if path[-18:-6] == f'{label}_2':
            twos.append(path)
'''
#Writing donor 1 and donor 3??? No idea how to make that happen          
