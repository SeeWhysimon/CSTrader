# For scripts tests
from scripts.data_processor.buff_processor import BuffDataProcessor

if __name__ == "__main__":
    processor = BuffDataProcessor()
    df = processor.load_data("./data/raw/buff_2025-05-24-15-24-00.json")

    cleaned_df = processor.clean_data(df)
    cleaned_df.to_csv("./data/processed/buff_cleaned.csv", index=False)