import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from math import pi


class DataVisualizer:
    def __init__(self,api_url="http://127.0.0.1:5000/api/students/"):
        self.api_url=api_url
        self.data = self.fetch_student_data_from_api()

    def fetch_student_data_from_api(self):
        try:
            print(f"[fetch_student_data_from_api]: Fetching data from {self.api_url} ...")
            response = requests.get(self.api_url,timeout=10)
            response.raise_for_status()
            data= response.json()['data']
            # data = [
            #     {"id": 101, "name": "Alice", "scores": {"Math": 90, "Science": 85, "English": 88, "History": 92}},
            #     {"id": 102, "name": "Bob", "scores": {"Math": 75, "Science": 80, "English": 70, "History": 65}},
            #     {"id": 103, "name": "Charlie", "scores": {"Math": 60, "Science": 95, "English": 80, "History": 78}},
            #     {"id": 104, "name": "Diana", "scores": {"Math": 95, "Science": 98, "English": 92, "History": 88}},
            #     {"id": 105, "name": "Evan", "scores": {"Math": 55, "Science": 60, "English": 45, "History": 50}},
            #     {"id": 105, "name": "Shivam", "scores": {"Math": 100, "Science": 100, "English": 100, "History": 100}}
            # ]
            return data
        except Exception as e:
            print("[fetch_student_data_from_api]: Fetching Data =>",e)
            return None

    def _process_data(self):

        try:
            print("[_process_data]: Converting into DataFrame")
            flat_data = []
            json_data = self.data
            
            for student in json_data:
                row = {"Name": student["name"]}
                row.update(student["scores"]) 
                flat_data.append(row)

            df = pd.DataFrame(flat_data)
            df.set_index("Name", inplace=True)
            df["Average"] = df.mean(axis=1)
            return df
        except Exception as e:
            print(f"[_process_data]: Error at processing data {e}")
            return None

    def visualize_data(self):
        print("[visualize_data]: Visualizeing Data ")
        df = self._process_data()
        try:
            fig = plt.figure(figsize=(16, 12), layout="constrained")
            plt.suptitle("Student Performance Dashboard", fontsize=16, weight='bold')

            df_scores = df.drop(columns=["Average"])
            
            # CHART 1
            ax1 = fig.add_subplot(221)
            df_scores.plot(kind='bar', ax=ax1, width=0.8)
            ax1.set_title("1. Subject-wise Comparison (Grouped Bar)", fontsize=12)
            ax1.set_ylabel("Score")
            ax1.set_ylim(0, 110)
            ax1.legend(loc='lower right', fontsize='small')
            plt.xticks(rotation=0)
            # CHART 1: Ends Here 

            #CHART 2: 
            ax2 = fig.add_subplot(222)
            df_scores.plot(kind='bar', stacked=True, ax=ax2, colormap='viridis', alpha=0.9)
            ax2.set_title("2. Cumulative Score Contribution (Stacked Bar)", fontsize=12)
            ax2.set_ylabel("Total Accumulated Points")
        
            # Adding labels inside the Graph
            for c in ax2.containers:
                ax2.bar_label(c, label_type='center', fontsize=8, color='white')
            plt.xticks(rotation=0)
            #CHART 2 Ends here 

            # Chart 3 write a line graph 
            ax3=fig.add_subplot(223)
            ax3.set_title("3. Average Marks Comprison ", fontsize=12)
            ax3.plot(df.index,df['Average'],marker='o',linewidth=5,markersize=10)

            #Cahrt 4 
            ax4 = fig.add_subplot(224)
            cax = ax4.imshow(df_scores.values, cmap='RdYlGn', aspect='auto', vmin=40, vmax=100)
            
            ax4.set_xticks(np.arange(len(df_scores.columns)))
            ax4.set_yticks(np.arange(len(df_scores.index)))
            ax4.set_xticklabels(df_scores.columns)
            ax4.set_yticklabels(df_scores.index)
            
            for i in range(len(df_scores.index)):
                for j in range(len(df_scores.columns)):
                    text = ax4.text(j, i, df_scores.values[i, j],
                                ha="center", va="center", color="black", weight='bold')
                    
            ax4.set_title("4. Class HeeatMap (Green=High, Red=Low)", fontsize=12)
            fig.colorbar(cax, ax=ax4, orientation='vertical', label='Score')

            # plt.tight_layout(rect=[0, 0.03, 1, 0.95]) 
            plt.show()
        except Exception as e:
            print("[visualize_data]: Error at Visualizer  ",e)
            
if __name__ == "__main__":
    data = DataVisualizer()
    print(data._process_data())
    data.visualize_data()