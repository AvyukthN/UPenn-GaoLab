import pandas as pd
from Bio import SeqIO

def populate_trin():
    nuc_hash = {
        0: "A",
        1: "C",
        2: "G",
        3: "T"
    }

    trinhash = {}
    C_list = []
    T_list = []
    for i in range(4**2):
        C_string = f"{nuc_hash[i // 4]}C{nuc_hash[i % 4]}"
        T_string = f"{nuc_hash[i // 4]}T{nuc_hash[i % 4]}"
        trinhash.update({C_string: 0})
        trinhash.update({T_string: 0})
        C_list.append(C_string)
        T_list.append(T_string)

    return trinhash, C_list, T_list

def load_fasta(fasta_file):
    # Load the entire FASTA file into a dictionary for quick access
    fasta_dict = {}
    for record in SeqIO.parse(fasta_file, "fasta"):
        fasta_dict[record.id] = record.seq
    return fasta_dict

def extract_trimer(seq_dict, location):
    # Parse the location string
    chromosome, pos_range = location.split(':')
    start_pos, end_pos = map(int, pos_range.split('-'))

    if start_pos != end_pos:
        raise ValueError(f"Start and end positions should be the same for location: {location}")

    # Identify the relevant sequence in the dictionary
    for key in seq_dict:
        chrom_key, range_key = key.split(':')
        start_range, end_range = map(int, range_key.split('-'))
        
        # Check if the location falls within the sequence range
        if chrom_key == 'chr' + chromosome and start_range <= start_pos <= end_range:
            # Calculate the index relative to the sequence
            relative_pos = start_pos - start_range
            
            # Extract the trimer centered at the given location
            trimer_start = relative_pos - 1
            trimer_end = relative_pos + 1
            trimer = seq_dict[key][trimer_start:trimer_end+1]
            return str(trimer)
    
    # If no matching sequence is found
    raise ValueError(f"Location {location} not found in the provided sequences.")

def topCatCounter(df: pd.DataFrame, fasta_fp: str):
    locations = df["Location"]

    fasta_dict = load_fasta(fasta_fp)
    location_trimers = list(map(lambda x: extract_trimer(fasta_dict, x), locations))

    trin_hash, clist, tlist = populate_trin()

    clist_count = [0 for _ in clist]
    tlist_count = [0 for _ in tlist]

    for trimer in location_trimers:
        if len(trimer) != 3:
            continue
        if trimer[1] == "C":
            clist_count[clist.index(trimer)] += 1
        if trimer[1] == "T":
            tlist_count[tlist.index(trimer)] += 1

    final_trimer_vec = clist_count + tlist_count
    return clist + tlist, final_trimer_vec
