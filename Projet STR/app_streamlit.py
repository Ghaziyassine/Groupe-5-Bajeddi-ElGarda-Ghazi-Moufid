import streamlit as st
import plotly.express as px
from scheduling_algorithms import fcfs, sjf, rm, dm, llf, edf, sjf_preemptive
from datetime import datetime, timedelta
import json

# Title of the Streamlit Application
st.title("Simulation des Algorithmes de Planification")

# Select Algorithm
algorithm = st.selectbox(
    "Choisissez un algorithme",
    ["FCFS", "SJF", "SJF Préemptif", "RM", "DM", "LLF", "EDF"]
)

# Input Tasks
st.subheader("Entrez les tâches sous format JSON")
default_tasks = """[
    {"id": 1, "arrival_time": 0, "execution_time": 3, "deadline": 7, "period": 10},
    {"id": 2, "arrival_time": 2, "execution_time": 6, "deadline": 8, "period": 15},
    {"id": 3, "arrival_time": 4, "execution_time": 4, "deadline": 10, "period": 20}
]"""
tasks_input = st.text_area("Exemple de tâches :", default_tasks, height=200)

# Button to Run Simulation
if st.button("Simuler"):
    try:
        # Parse Input Tasks
        tasks = json.loads(tasks_input)

        # Run the selected algorithm
        if algorithm == "FCFS":
            schedule, steps = fcfs(tasks.copy())
        elif algorithm == "SJF":
            schedule, steps = sjf(tasks.copy())
        elif algorithm == "SJF Préemptif":
            schedule = sjf_preemptive(tasks.copy())
            steps = ["SJF Préemptif: La simulation s'est déroulée correctement."]
        elif algorithm == "RM":
            schedule, steps = rm(tasks.copy())
        elif algorithm == "DM":
            schedule, steps = dm(tasks.copy())
        elif algorithm == "LLF":
            schedule, steps = llf(tasks.copy())
        elif algorithm == "EDF":
            schedule, steps = edf(tasks.copy())
        else:
            st.error("Algorithme non reconnu.")
            schedule, steps = [], []

        # Display Simulation Results
        st.subheader("Résultats de la Simulation")
        st.write("**Calendrier des tâches :**")
        st.json(schedule)

        st.write("**Étapes de l'algorithme :**")
        for step in steps:
            st.write(f"- {step}")

        # Prepare Gantt Chart Data
        gantt_data = []
        base_time = datetime(1970, 1, 1)  # Reference time
        for task in schedule:
            gantt_data.append({
                "Tâche": f"Tâche {task['task']}",
                "Début": base_time + timedelta(seconds=task["start"]),
                "Fin": base_time + timedelta(seconds=task["end"])
            })

        # Plot Gantt Chart
        st.subheader("Diagramme de Gantt")
        if gantt_data:
            fig = px.timeline(
                gantt_data,
                x_start="Début",
                x_end="Fin",
                y="Tâche",
                title=f"Diagramme de Gantt - {algorithm}",
                labels={"Tâche": "Tâches"}
            )
            fig.update_yaxes(categoryorder="total ascending")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Aucune donnée pour générer le diagramme de Gantt.")

    except Exception as e:
        st.error(f"Erreur : {e}")
