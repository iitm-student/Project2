# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests",
#   "pandas",
#   "seaborn",
#   "matplotlib",
# ]
# ///

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import requests
import os
import sys
import json
from typing import Dict, Any

class AUTOLYSIS:
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.df = pd.read_csv(dataset_path, encoding='latin-1')
        self.ai_proxy_token = os.environ.get("AIPROXY_TOKEN")
        if not self.ai_proxy_token:
            raise ValueError("There's no token")
        
        self.base_url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

    def get_summary(self) -> Dict[str, Any]:
      zeroes = self.df.isnull().sum()
      zeroes = zeroes[zeroes!=0]
      
      summary = {
          "rows": self.df.shape[0],
          "columns": self.df.shape[1],
          "missing_values": zeroes.to_dict(),
          "columns": [{"name": col, "type": str(self.df[col].dtype)} for col in self.df.columns],
          "desc": self.df.describe().to_dict()
      }
      return summary

    def generate_visualizations(self, autolysis_output: Dict[str, Any]):
      #data prep
      numeric_df = selfdf.select_dtypes(include=['number'])
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
      
    def storytime(self, autolysis_output: Dict[str, Any]) -> str:
        prompt = f"Analyze the following data summary and tell a story about the data (Use Markdown formatting):\n{summary}"

        data = {
          "model": "gpt-4o-mini",
          "messages":[
                      {"role": "system", "content": "You are a data analyst."},
                      {"role": "user", "content": prompt}
                  ]}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.ai_proxy_token}"
        }

        response = requests.post(self.base_url, headers=headers, json=data)
            
        if response.status_code == 200:
          data = response.json()
          print("Success")
          return data.get('choices', [{}])[0].get('message', {}).get('content', 'No message content available')
        else:
          print(f"Error: {response.status_code}:{response.text}")
          return "Error"

    def run(self):
        autolysis_output = self.get_summary()
        self.visualization(autolysis_output)
        story = self.storytime(autolysis_output)
        
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(story)

def main():
    analysis.run()

if __name__ == "__main__":
    main()
