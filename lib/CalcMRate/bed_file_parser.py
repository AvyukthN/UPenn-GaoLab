from pybedtools import BedTool

regions = BedTool('./human_genome_regions.bed')

print(type(regions))