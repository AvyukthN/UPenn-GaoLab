from StrategyInterfaces import ExtractStratergy, TransformStrategy, LoadStrategy

class CSVExtractStrategy(ExtractStrategy):
    def extract(self, source):
        # CSV EXTRACTION LOGIC
        # takes in csv of gene names and COSMIC sig.s and returns list of them for transform strategies
        pass

class TSVExtractStrategy(ExtractStrategy):
    def extract(self, source):
        # TSV EXTRACTION LOGIC
        # takes in tsv of gene names and COSMIC sig.'s and returns list of them for transform strategies
        pass

class UniversalTransformStrategy(TransformStrategy):
    def transform(self, extracted_data):
        # take in list of gene names & COSMIC sig.'s
        # transform into list of lists
        # [[*gene_name*, *COSMIC sig.*, *Susceptibility Score*, ...], ...]
        pass

class CSVLoadStrategy(LoadStrategy):
    def load(self, transformed_data, destination):
        # takes in output list of lists defined in Universal Transform Strategy and saves in CSV format at destination filepath
        pass

class TSVLoadStrategy(LoadStrategy):
    def load(self, transformed_data, destination):
        # takes in output list of lists defined in Universal Transform Strategy and saves in TSV format at destination filepath
        pass
