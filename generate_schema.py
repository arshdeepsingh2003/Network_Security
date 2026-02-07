import pandas as pd
import yaml
import os

# Read training data
df = pd.read_csv(
    "Artifacts/data_ingestion/ingested_data/train.csv"
)

# Build schema
schema = {
    "columns": [{col: "int64"} for col in df.columns],
    "numerical_columns": list(df.columns)
}

# Ensure schema directory exists
os.makedirs("data_schema", exist_ok=True)

# Write schema to correct location
with open("data_schema/schema.yaml", "w") as f:
    yaml.dump(schema, f, sort_keys=False)

print("✅ schema.yaml updated with", len(df.columns), "columns")
