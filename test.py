# For scripts tests
from scripts.pipeline.random_forest_pipeline import RandomForestPipeline

if __name__ == "__main__":
    pipeline = RandomForestPipeline()
    pipeline.run()
