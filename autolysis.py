import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import requests

def get_summary(df):
  zeroes = df.isnull().sum()
  zeroes = zeroes[zeroes!=0]
  
  summary = {
      "rows": df.shape[0],
      "columns": df.shape[1],
      "missing_values": zeroes.to_dict(),
      "columns": [{"name": col, "type": str(df[col].dtype)} for col in df.columns],
      "desc": df.describe().to_dict()
  }
  return summary

def visualization(df):
    #data prep
    numeric_df = df.select_dtypes(include=['number'])
    drop_col = [col for col in numeric_df.columns if col.lower().endswith('id')]
    numeric_df = numeric_df.drop(columns=drop_col, inplace=False).dropna(axis=1, how='all')
    numeric_df = numeric_df.fillna(0)

    # correlation heatmap
    if numeric_df.shape[1] > 1:
        plt.figure(figsize=(12, 8))
        correlation_matrix = numeric_df.corr()
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm')
        plt.title('Correlation Heatmap')
        plt.tight_layout()
        plt.savefig('correlation_heatmap.png', dpi=100)
        plt.close()

import numpy as np
import requests

PROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
AIPROXY_TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIyZjMwMDIxOTJAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.Ur4b3j-7w3C4TTs32l4TxANcvtRTfOqJ2Yv5ge4ynlc'

prompt = f"Analyze the following data summary and tell a story about the data:\n{summary}"
# Send summary to ChatGPT
def send_summary(model):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AIPROXY_TOKEN}"
    }
    data = {
        "model": model,
        "messages":[
                    {"role": "system", "content": "You are a data analyst."},
                    {"role": "user", "content": prompt}
                ],
    }
    response = requests.post(PROXY_URL, headers=headers, json=data)
    if response.status_code == 200:
        data = response.json()
        print("Success!")
        return response['choices'][0]['message']['content'].strip()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return f"Error generating response: {response.status_code}"
    # Distribution of numeric columns
    plt.figure(figsize=(12, 6))
    sampled_df = numeric_df.sample(n=1000, random_state=42) if len(numeric_df) > 1000 else numeric_df
    for i, col in enumerate(sampled_df.columns[:3], 1):
        plt.subplot(1, 3, i)
        sns.histplot(sampled_df[col], kde=True, color='blue')
        plt.title(f'Distribution of {col}')
    plt.tight_layout()
    plt.savefig('numeric_distributions.png', dpi=100)
    plt.close()
m ="gpt-4o-mini"
info = send_summary(m)


