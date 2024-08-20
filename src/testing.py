from Context import pipelineContext

pc = pipelineContext()

pc.createPipeline("./testing_data/gene_list.csv", "./testing_data/out")
pc.execute()
