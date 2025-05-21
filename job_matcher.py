import pandas as pd
from fuzzywuzzy import fuzz

JOBS_CSV = 'jobs/jobs.csv'

def match_jobs(profile):
    jobs_df = pd.read_csv(JOBS_CSV)
    user_skills = set([s.lower() for s in profile.get('skills', [])])
    scores = []
    gaps = []
    for _, job in jobs_df.iterrows():
        job_skills = set(str(job['Skills']).lower().split(','))
        match_count = len(user_skills & job_skills)
        total = len(job_skills)
        score = int((match_count / total) * 100) if total else 0
        scores.append(score)
        missing = list(job_skills - user_skills)
        gaps.append(missing)
    jobs = jobs_df.to_dict(orient='records')
    return jobs, scores, gaps 