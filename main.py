# scripts/main.py

from scripts.pipeline.random_forest_pipeline import RandomForestPipeline

if __name__ == "__main__":
    pipeline = RandomForestPipeline()
    pipeline.run(config_path="./scripts/data_collector/steamdt/steamdt_config.json")