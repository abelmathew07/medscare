from datasets import load_dataset
import pandas as pd

# Load the dataset
dataset = load_dataset("QuyenAnhDE/Diseases_Symptoms")

# Convert to pandas DataFrame
df = pd.DataFrame(dataset)

# Save DataFrame to CSV
df.to_csv('full_diseases.csv', index=False)
