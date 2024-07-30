from StrategyInterfaces import ExtractStratergy, TransformStrategy, LoadStrategy

class SSETL():
    def __init__(self, extract_strategy: ExtractStrategy, transform_strategy: TransformStrategy, load_strategy: LoadStrategy):
        self.extract_strategy = extract_strategy
        self.transform_strategy = transform_strategy
        self.load_strategy = load_strategy

    def setExtractStrategy(self, extract_strategy: ExtractStrategy):
        self.extract_strategy = extract_strategy
    def setTransformStrategy(self, transform_strategy: TransformStrategy):
        self.transform_strategy = transform_strategy
    def setLoadStrategy(self, load_strategy: LoadStrategy):
        self.load_strategy = load_strategy

    def executePipeline(self, source, destination):
        extracted_data = self.extract_strategy.extract(source)
        transformed_data = self.transform_strategy.transform(extracted_data)
        self.load_strategy.load(transformed_data, destination)

if __name__ == '__main__':
    # Initialize with specific strategies
    pipeline = ETLPipeline(
        CSVExtractStrategy(),
        GeneTransformStrategy(),
        DatabaseLoadStrategy()
    )

    # Execute the pipeline
    pipeline.execute("input.csv", "database_connection")

    # Change strategies dynamically
    pipeline.set_extract_strategy(APIExtractStrategy())
    pipeline.set_transform_strategy(SignatureTransformStrategy())
    pipeline.set_load_strategy(FileLoadStrategy())

    # Execute with new strategies
    pipeline.execute("api_endpoint", "output.json")
