# Python-Pipeline-Vir-Trivedi
This is my Python Pipeline project (Track 2) for Dr. Wheeler's COMP 383 course, section 001, but even better.

Hello and welcome to my Python Pipeline project GitHub! If you're looking for a fun time, you've come to the right place.
My name is Vir Trivedi, and I will be your tour guide through this wacky wrapper script journey that is Track 2 of our Python Pipeline project.

Prior to running the script, there are a few important things to go over and discuss. It is imperative you read this carefully for accurate instruction and understanding.
Firstly, you must download the modules argparse, sys, BioPython, Entrez, os, subprocess, and glob. Each of these play a major role in the way the script runs. The script already contains the import statements for each of these modules and will call them on its own. All that is required on your end is that you have each of these already downloaded for import in your server.

Included in this repository is a python script titled "wrapper.py". This is the wrapper script that you will be using to run the whole pipeline in one go. Pretty nifty, right?

Running this script is pretty simple and can be done via the command line by entering:

'''
python {the parent directory that contains the cloned repository}/Python-Pipeline-Vir-Trivedi/wrapper.py --input {insert filepath here}
'''

^^Important to note: your --input should either be sampledata or fulldata. By inputting sampledata, the script will call the sampledata directory and use the sample fastq files (these only contain the first 10000 reads of the original fastq files found in fulldata.

As the code runs, during the BLAST+ portion, you may find that you are asked if you are willing to replace certain files. The answer is always yes.

<img width="728" alt="image" src="https://github.com/riv-eting/Python-Pipeline-Vir-Trivedi/assets/118252671/4663979d-f400-4775-bce8-e9c500dc0fcb">

Upon completion of the script, you can check the log file made inside of the PipelineProject_Vir_Trivedi directory housed in Python-Pipeline-Vir-Trivedi.

WARNING: You may feel something like below once you have finished running all the code:

![Alt Text](https://giphy.com/gifs/paper-triangles-yes-sure-approve-mCIjCgs3nWQWfJZvPA/giphy.gif)


