import Bio
import os
import glob
import subprocess
from Bio import Entrez
from Bio import SeqIO
#The above modules are imported for use in the pipeline --> subprocess and os are used to run bash commands from the python script itself while Bio, SeqIO, and Entrez are BioPython tools meant to be used to process sequence data and extract it from NCBI remotely from this script
host=os.getcwd()
#We store the user's current working directory as a variable using os.getcwd to help create generalized paths for whoever wishes to run this script
log=open(f'{host}/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/PipelineProject.log', 'a')
print(host)
inpath = f'{host}/Python-Pipeline-Vir-Trivedi/sampledata/*SRX*.fastq'
#inpath is a variable defined that contains the file path location of the original fastq files
fastqs = glob.glob(inpath)
#fastqs is a list of all fastq paths from the directory being used created from glob.glob
fastq_labels=[]
for path in fastqs:
    fastq_labels.append(path[-18:-8])
fastq_labels=set(fastq_labels)
#The above loop iterates over each of the file paths stored in fastqs and isolates their specific SRX labels in a set
#This set will allow us to isolate paired fastq files and run them through bowtie
Entrez.email='vtrivedi1@luc.edu'
ID = 'NC_006273.2'
handle=Entrez.efetch(db='nucleotide',id=ID,rettype='fasta',retmode='text')
index_fasta = f'{ID}.fna'
with open(index_fasta, 'w') as w:
    w.write(handle.read())
#To get the fna file (NC_006273.2) for indexing, I used entrez efetch using the nucleotide database and the NC accession number
#This fna file is fected from the nucleotide database as a fasta file and is then written to the index_fasta file created
os.system('bowtie2-build ' + index_fasta + ' HCMV')
#The above os.system call is used to build an index for Bowtie to run later on
#We use the HCMV index and build it out using the fasta file we created just above
ones=[]
twos=[]
for path in fastqs:
    if path[-7]=='1':
        ones.append(path)
    if path[-7]=='2':
        twos.append(path)
#The above loop iterates over the file paths inputted for the SRA fastq files and sorts them into two separate lists depending on whether they contain '_1' or '_2'. This separates the forward fastq and reverse fastq of a pair of fastqs for one sequence
for label in fastq_labels:
    for first in ones:
        if first[-18:-8] == f'{label}':
            a = first
    for second in twos:
        if second[-18:-8] == f'{label}':
            b = second
    host=os.getcwd()
    os.system(f'bowtie2 -x HCMV -1 ' + a + ' -2 ' + b + ' -S ' + label + f'.sam --al-conc {host}/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/sample_' + label + '_mapped_%.fq')
#This next set of nested for loops above iterates over the SRA sequence labels and checks them with the ones and twos lists generated prior
#After identifying the corresponding fastq file in each list, _1.fastq is assigned to variable 'a' and _2.fastq is assigned to variable 'b'
#For each 'a' and 'b' pair, bowtie 2 is run --> as a result, bowtie 2 is run for the paired end fastq files of each separate sequence downloaded
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
#Above, we create a dictionary that assigns the labels on each pair of fastq files we made to the donor origin --> this will be useful when we write the number of reads in the original fastq files and mapped fastq files per donor
mapped = glob.glob(f'{host}/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/sample_SRX*_mapped*.fq')
#We create a list called mapped that contains all the paths to the mapped fastq files produced from Bowtie
total_reads=list(mapped+fastqs)
#total_reads is a list that contains all file paths for the original fastq files and all the fastq files of the reads that mapped in bowtie
host=os.getcwd()
#We re define host as the current working directory to implement in future paths
for label in fastq_labels:
    precount_1=0
    precount_2=0
    count_1=0
    count_2=0
    #This first for loop iterates over the labels in fastq_labels --> we will then search total_reads to find all mapped fastq and original fastq files
    #We establish two precount values to be used to track the number of reads in each original fastq file
    #We establish two count values to be used to track the number of reads in each mapped fastq file
    for file in total_reads:
        #This for iterates over each file path in total_reads for each label to identify the four files (2 mapped and 2 original paired end fastqs) that correspond with the label the outer loop is processing at the time
        if file == f'{host}/Python-Pipeline-Vir-Trivedi/sampledata/sample_{label}_1.fastq':
            with open(file, 'r') as f1:
                lines=f1.readlines()
                precount_1 = (len(lines)/4)
        if file == f'{host}/Python-Pipeline-Vir-Trivedi/sampledata/sample_{label}_2.fastq':
            with open(file, 'r') as f2:
                lines=f2.readlines()
                precount_2 = (len(lines)/4)
        #The above if statements check to see if the file from total_reads matches either the forward end (_1) or reverse end (_2) of which ever label the outer loop is iterating over
        #Here, the lines are counted in each identified file by opening the file as a text file and creating a variable of readlines associated with it
        #If it matches one of them, the associated precount variable is updated to reflect the number of reads from that file by taking the number of lines in the file and dividing by 4
        #We divide by 4 because each read in a fastq file is represented by 4 lines (identifier, sequence, phred quality score, and a comment line)
        if file == f'{host}/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/sample_{label}_mapped_1.fq':
            command = f'wc -l {file}'
            count_1 = subprocess.check_output(command, shell=True, universal_newlines=True)
            count_1 = str(count_1)
            c_1 = count_1.split(' ')
            count_1 = (int(c_1[0]))/4
        if file == f'{host}/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/sample_{label}_mapped_2.fq':
            command = f'wc -l {file}'
            count_2 = subprocess.check_output(command, shell=True, universal_newlines=True)
            count_2 = str(count_2)
            c_2 = count_2.split(' ')
            count_2 = (int(c_2[0]))/4
        #The above two if statements are used to identify if any of the files iterated over match the mapped fastq files corresponding to which ever label the outer loop is iterating over at the moment
        #Then, using subprocess.check_output, we check the line count in the file by using wc -l as a bash command through subprocess
        #This command's result is assigned to a count_* variable that is then converted into a string that contains the line count and file path in one string separated by a space
        #To isolate the line count, .split(' ') is used to create a two item list of strings, and the first item (the count) is isolated, divided by 4, and assigned to the count_* variable
    log.write(f'{fastq_donor_dict[label]} had {precount_1 + precount_2} reads before Bowtie2 filtering and {count_1 + count_2} read pairs after.\n')
    #For each label iterated over, 4 fastq files are identified. To receive the total number of reads prior to mapping we add precount_1 and precount_2 --> these are the read counts from the original fastq files determined among the first two if statements in the inner loop
    #To receive the total number of reads after mapping, we add count_1 and count_2, which are the read counts of the mapped fastq files
    #These sums are inputted into a format string that writes to our log file how many original reads and mapped reads there were per donor/dpi pair
    #The donor/dpi pair is retrieved by using the label iterated over in the outer loop as an index for the dictionary made in lines 53-61
os.system(f'spades.py -k 127 --only-assembler --pe1-1 {host}/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/sample_SRX2896360_mapped_1.fq --pe1-2 {host}/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/sample_SRX2896360_mapped_2.fq --pe2-1 {host}/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/sample_SRX2896363_mapped_1.fq --pe2-2 {host}/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/sample_SRX2896363_mapped_2.fq --pe3-1 {host}/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/sample_SRX2896374_mapped_1.fq --pe3-2 {host}/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/sample_SRX2896374_mapped_2.fq --pe4-1 {host}/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/sample_SRX2896375_mapped_1.fq --pe4-2 {host}/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/sample_SRX2896375_mapped_2.fq -o {host}/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/')
#The above os.system call runs SPades to assemble a genome using all 8 mapped fastq files by referencing their paths
#All output of SPades is sent to the PipelineProject_Vir_Trivedi directory
above_thousand = 0
above_thous_lst = []
with open(f'{host}/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/contigs.fasta', 'r') as f:
    for record in SeqIO.parse(f, 'fasta'):
        if len(record.seq) > 1000:
            above_thousand += 1
            above_thous_lst.append(len(record.seq))
#The above with open statement and its inner loop open the contigs file produced by the SPades command, parse it, and compare the lengths of each contig to a baseline level of 1000 base pairs
#If a read is longer than 1000 base pairs, the variable above_thousand increases in value by 1 so as to track the number of contigs greater than 1000 bp. Additionally, the length of the sequence is appended to the list above_thous_lst to track the lengths of each >1000 bp length sequence
log.write(f'There are {above_thousand} contigs > 1000 bp in the assembly\n')
log.write(f'There are {sum(above_thous_lst)} bp in the assembly\n')
#The above log.write commands write the number of sequences with lengths > 1000bp to the log file as well as the sum of all of those lengths
host=os.getcwd()
#host is redefined to confirm that the current working directory is the user's home directory
contig_lengths={}
with open(f'{host}/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/contigs.fasta', 'r') as f:
    for record in SeqIO.parse(f, 'fasta'):
        contig_lengths[len(record)]=record.id
#Above, the contigs file outputted from SPades is opened, having the length of each contig written as a key to a dictionary (contig_lengths) with the associated contig id as a value
max_len = max(contig_lengths)
max_record = contig_lengths[max_len]
#Using the contig lengths dictionary, the maximum length is found by taking the max() of the keys and stored in max_len. Then, the id of that longest sequence is taken by finding the associated value of max_len within the contig_lengths dictionary
with open(f'{host}/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/contigs.fasta', 'r') as f:
    for record in SeqIO.parse(f, 'fasta'):
        if max_record == record.id:
            with open(f'{host}/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/Betaherpesvirinae.fasta', 'a') as w:
                w.write(f'>{str(record.id)}\n')
                w.write(str(record.seq))
#The above with open statement opens up the SPades contigs output file again and parses through each record --> if a record is found whose id matches the id of the longest sequence identified above as max record, then a new file is opened called Betaherpesvirinae.fasta within the PipelineProject_Vir_Trivedi directory to which the sequence and id of the largest contig is written
os.system('datasets download virus genome taxon Betaherpesvirinae --include genome')
#A reference genome is downloaded to be used to make a local BLAST+ database for Betaherpesvirinae
os.system('unzip ncbi_dataset.zip')
#The reference genome and other files are stored within a zipped directory called ncbi_dataset.zip --> this directory is unzipped
os.system('makeblastdb -in ncbi_dataset/data/genomic.fna -out BetaHerp -title BetaHerp -dbtype nucl')
#A BLAST+ database called BetaHerp is created using the genome fasta file taken from NCBI in the datasets download command
blastcmd = f'blastn -query {host}/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/Betaherpesvirinae.fasta -db BetaHerp -out {host}/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/betaherpesvirinaeblast.csv -outfmt "6 sacc pident length qstart qend sstart send bitscore evalue stitle" -max_hsps 1'
#The above blastcmd variable stores the blast command to be run, specifying the Betaherpesvirinae.fasta file as the query, the BetaHerp database as the database, and a specified file path for the file to be generated from the blast command. The command is designed to generate a tab separated values file that specifies  Subject accession, Percent identity, Alignment length, Start of alignment in query, End of alignment in query, Start of alignment in subject, End of alignment in subject, Bit score, E-value, and Subject Title
os.system(blastcmd)
#This os.system command runs the blast command
headers=['sacc', 'pident', 'length', 'qstart', 'qend', 'sstart', 'send', 'bitscore', 'evalue', 'stitle\n']
#A list of headers that corresponds with  Subject accession, Percent identity, Alignment length, Start of alignment in query, End of alignment in query, Start of alignment in subject, End of alignment in subject, Bit score, E-value, and Subject Title is created
log.write('\t'.join(headers))
#The list is converted into a string with each item separated by a tab. This string is written to the log file
f=open(f'{host}/Python-Pipeline-Vir-Trivedi/PipelineProject_Vir_Trivedi/betaherpesvirinaeblast.csv', 'r')
blast=f.read().rstrip().split('\n')
log.write('\n'.join(blast[0:10]))
#The BLAST+ result file is opened, with each hit being separated into an item in a list titled blast
#From the list blast, the top ten hits are written to the log file as one string with each hit separated by a new line value
