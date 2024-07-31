from ConcreteStratergies import CSVExtractStrategy, TSVExtractStrategy, UniversalTransformStrategy, CSVLoadStrategy, TSVLoadStrategy
from SusceptibilityScoreETL import SSETL

class pipelineContext:
    def __init__(self):
        self.pipeline = SSETL();
        self.source = None
        self.destination = None

    def createPipeline(self, source, destination):
        source_ext = source.split(".")[-1]
        dest_ext = destination.split(".")[-1]

        self.source = source 
        self.destination = destination 

        match source_ext:
            case "csv":
                self.pipeline.setExtractStrategy(CSVExtractStrategy())
            case "tsv":
                self.pipeline.setExtractStrategy(TSVExtractStrategy())

        match dest_ext:
            case "csv":
                self.pipeline.setLoadStrategy(CSVLoadStrategy())
            case "tsv":
                self.pipeline.setLoadStrategy(TSVLoadStrategy())

        self.pipeline.setTransformStrategy(UniversalTransformStrategy())

    def execute(self):
        self.pipeline.executePipeline(self.source, self.destination)
