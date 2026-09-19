import pandas as pd
import numpy as np

from langchain_core.tools import tool


df = pd.read_csv("data/students.csv")


@tool
def analyze_student(student_name: str):
    """
    Analyze a student's skills using Pandas and NumPy.
    Use this tool when the user asks about a specific student's
    performance, skills, strengths, weaknesses or skill gaps.
    """

    student = df[
        df["name"].str.lower() == student_name.lower()
    ]

    if student.empty:
        return f"Student {student_name} was not found."

    student = student.iloc[0]

    skills = [
        "python",
        "pandas",
        "numpy",
        "sql",
        "excel",
        "statistics",
        "machine_learning"
    ]

    scores = [
        student[skill]
        for skill in skills
    ]

    average = np.mean(scores)

    weak_skills = [
        skill
        for skill in skills
        if student[skill] < 60
    ]

    strong_skills = [
        skill
        for skill in skills
        if student[skill] >= 75
    ]

    return {
        "student": student_name,
        "average_score": round(float(average), 2),
        "strong_skills": strong_skills,
        "weak_skills": weak_skills,
        "scores": {
            skill: int(student[skill])
            for skill in skills
        }
    }


@tool
def compare_students(student1: str, student2: str):
    """
    Compare two students using their skill scores.
    """

    s1 = df[
        df["name"].str.lower() == student1.lower()
    ]

    s2 = df[
        df["name"].str.lower() == student2.lower()
    ]

    if s1.empty or s2.empty:
        return "One or both students were not found."

    s1 = s1.iloc[0]
    s2 = s2.iloc[0]

    skills = [
        "python",
        "pandas",
        "numpy",
        "sql",
        "excel",
        "statistics",
        "machine_learning"
    ]

    comparison = {}

    for skill in skills:

        difference = (
            int(s1[skill]) -
            int(s2[skill])
        )

        comparison[skill] = {
            student1: int(s1[skill]),
            student2: int(s2[skill]),
            "difference": difference
        }

    return comparison