import openai
import random
import copy
import json
import os
import csv
from ses import api_key, base_url
import pandas as pd

# Load the two CSV files
df1 = pd.read_csv('dpo_abstract.csv')
df2 = pd.read_csv('grpo_abstract.csv')

# Ensure the columns are in the same order by reordering them to match one of the files
df2 = df2[df1.columns]

# Concatenate the DataFrames
df_combined = pd.concat([df1, df2], ignore_index=True)
paper_dict_list = df_combined.to_dict(orient='records')

# Read the template prompt from the file
with open("label_prompt.txt", "r") as f:
  template = "".join(f.readlines())

# OpenAI client setup
client = openai.OpenAI(api_key=api_key, base_url=base_url)

# Define the output CSV file
output_file = 'labeled_papers.csv'

# Write header to the CSV file (if not exists)
header = [
    'Title', 'Cited By', 'URL', 'Abstract', 'Category', 'Importance',
    'Explanation'
]
if not os.path.exists(output_file):
  with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)

# Loop through each paper and make API calls
for i, entry in enumerate(paper_dict_list):
  # Prepare the prompt for the model
  prompt = template + f"Title: {entry['Title']}\nCited By: {entry['Cited By']}\nURL: {entry['URL']}\nAbstract: {entry.get('Abstract', '')}\n"

  # Get the response from OpenAI
  chat_completion = client.chat.completions.create(
      messages=[
          {
              "role": "user",
              "content": prompt
          },
      ],
      model="gpt-4",
      response_format={"type": "json_object"},
  )

  res = chat_completion.choices[0].message.content.strip()

  # Parse the response as a JSON object
  try:
    res_json = json.loads(res)
    # Extract the necessary fields
    category = res_json.get('Category', '')
    importance = res_json.get('Importance', '')
    explanation = res_json.get('Explanation', '')
  except json.JSONDecodeError:
    category = importance = explanation = 'Error parsing response'

  # Prepare the data to be written to CSV (entry data + response)
  row = [
      entry['Title'], entry['Cited By'], entry['URL'],
      entry.get('Abstract', ''), category, importance, explanation
  ]

  # Write to CSV incrementally
  with open(output_file, 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(row)

  print('*' * 50)
  print(i / len(paper_dict_list))
  print(row)
