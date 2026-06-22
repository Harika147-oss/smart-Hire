import pandas as pd

def recommend_jobs():

    jobs = pd.read_csv("data/jobs.csv")

    return jobs