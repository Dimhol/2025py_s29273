# Purpose: Generate a random DNA sequence in FASTA format with user inputs
# Context: Exercise for bioinformatics course. Prompts user for sequence
#    length, ID, description, and name. Inserts student name (excluded
#    from statistics) at a random position, calculates nucleotide
#    frequencies and CG ratio, wraps sequence lines to 60 bp, and
#    saves to a FASTA file named {ID}.fasta.

import random      # for generating random nucleotides and insertion position
import textwrap   # for wrapping FASTA sequence lines at 60 characters
import sys         # for exiting program on input errors
import os          # for checking if output file already exists


# ORIGINAL: length = int(input("Enter the sequence length: "))
# MODIFIED (Added input validation to ensure a positive integer):
while True:
    try:
        length_input = input("Enter the sequence length: ")  # prompt for sequence length
        length = int(length_input)                           # convert to integer
        if length <= 0:
            raise ValueError("Length must be a positive integer")
        break
    except ValueError as e:
        print(f"Invalid input ({e}). Please enter a positive integer.")


# ORIGINAL: seq_id = input("Enter the sequence ID: ")
# MODIFIED (Strip whitespace and replace invalid filename characters):
raw_id = input("Enter the sequence ID: ")                  # prompt for sequence ID
seq_id = raw_id.strip().replace("/", "_").replace("\\", "_").replace(" ", "_")


# ORIGINAL: description = input("Provide a description of the sequence: ")
# MODIFIED (Strip leading and trailing whitespace):
description = input("Provide a description of the sequence: ").strip()


# ORIGINAL: name = input("Enter your name: ")
# MODIFIED (Ensure non-empty name and strip whitespace):
name = input("Enter your name: ").strip()
if not name:
    print("Name cannot be empty. Exiting.")
    sys.exit(1)


# Generate the core DNA sequence without the inserted name
dna_core = ''.join(random.choice(['A', 'C', 'G', 'T']) for _ in range(length))


# Insert the name at a random position (excluded from statistics)
insert_pos = random.randint(0, len(dna_core))          # random insertion position
full_sequence = dna_core[:insert_pos] + name + dna_core[insert_pos:]


# ORIGINAL: filename = f"{seq_id}.fasta"
# MODIFIED (Check for existing file and confirm overwrite):
filename = f"{seq_id}.fasta"                             # output FASTA filename
if os.path.exists(filename):
    overwrite = input(f"File {filename} already exists. Overwrite? (y/n): ").strip().lower()
    if overwrite != 'y':
        print("Operation cancelled.")
        sys.exit(0)

# Write the FASTA file: header and wrapped sequence lines
with open(filename, 'w') as fasta_file:
    fasta_file.write(f">{seq_id} {description}\n")
    fasta_file.write(textwrap.fill(full_sequence, width=60) + "\n")


# Calculate statistics based on dna_core (excluding the inserted name)
count_A = dna_core.count('A')  # count of A nucleotides
count_C = dna_core.count('C')  # count of C nucleotides
count_G = dna_core.count('G')  # count of G nucleotides
count_T = dna_core.count('T')  # count of T nucleotides
total   = len(dna_core)        # total nucleotides (should equal length)

# Calculate percentage frequencies
pct_A  = count_A / total * 100
pct_C  = count_C / total * 100
pct_G  = count_G / total * 100
pct_T  = count_T / total * 100
pct_CG = pct_C + pct_G        # combined C+G percentage


print(f"\nSequence saved to {filename}\n")
print("Sequence statistics:")
print(f"A: {pct_A:.1f}%")
print(f"C: {pct_C:.1f}%")
print(f"G: {pct_G:.1f}%")
print(f"T: {pct_T:.1f}%")
print(f"%CG: {pct_CG:.1f}%")
