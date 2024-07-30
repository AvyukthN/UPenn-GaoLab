from abc import ABC, abstractmethod

# essentially a blueprint for the concrete strategy classes to follow
class ExtractStrategy(ABC):
    @abstractmethod
    def extract(self, source):
        pass

class TransformStrategy(ABC):
    @abstractmethod
    def transform(self, extracted_data):
        pass

class LoadStrategy(ABC):
    @abstractmethod
    def load(self, transformed_data, destination):
        pass
