import pandas as pd
from urllib.parse import urlparse

# Load CSV file
csv_path = './grpo_citations.csv'
csv_path = './dpo_citations.csv'
df = pd.read_csv(csv_path)

# Extract domain from URLs
df['Domain'] = df['URL'].apply(lambda x: urlparse(x).netloc.split('.')[-2])

# Count frequency of each domain
domain_counts = df['Domain'].value_counts().reset_index()
domain_counts.columns = ['Domain', 'Frequency']
print(domain_counts)
