from Context import pipelineContext

pc = pipelineContext()

pc.createPipeline("./testing_data/test.csv", "./testing_data/out")
pc.execute()
