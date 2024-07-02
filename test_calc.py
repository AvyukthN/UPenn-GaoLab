import numpy as np
from CalcMRate2 import CalcMRate

c = CalcMRate("./bed_data/test.bed", "./fasta_data/hg38.fa", "./extraction_dir", "extracted_test", np.random.rand(96))
c.get_spec32()
