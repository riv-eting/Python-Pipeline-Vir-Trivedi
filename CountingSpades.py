import Bio
import os
import glob
from Bio import Entrez
from Bio import SeqIO
log=open('PipelineProject.log', 'w')
above_thousand = 0
above_thous_lst = []
with open('/home/vtrivedi1/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/contigs.fasta', 'r') as f:
    for record in SeqIO.parse(f, 'fasta'):
        if len(record.seq) > 1000:
            above_thousand += 1
            above_thous_lst.append(len(record.seq))
print(f'There are {above_thousand} contigs > 1000 bp in the assembly')
print(f'There are {sum(above_thous_lst)} bp in the assembly')
