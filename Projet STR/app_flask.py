from flask import Flask, request, render_template, jsonify
from scheduling_algorithms import fcfs, sjf, rm, dm, llf, edf
from datetime import datetime, timedelta
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        # Retrieve the data from the request
        data = request.json
        tasks = data.get('tasks', [])
        algorithm = data.get('algorithm', '')

        # Process the tasks using the selected algorithm
        if algorithm == "FCFS":
            result = fcfs(tasks)
        elif algorithm == "SJF":
            result = sjf(tasks)
        elif algorithm == "RM":
            result = rm(tasks)
        elif algorithm == "DM":
            result = dm(tasks)
        elif algorithm == "LLF":
            result = llf(tasks)
        elif algorithm == "EDF":
            result = edf(tasks)
        else:
            return jsonify({'error': "Algorithme non supporté."}), 400

        # Prepare Gantt chart data
        base_time = datetime(1970, 1, 1)
        gantt_data = []
        for task in result:
            gantt_data.append({
                "Task": f"Tâche {task['task']}",
                "Start": base_time + timedelta(seconds=float(task["start"])),
                "Finish": base_time + timedelta(seconds=float(task["end"])),
            })

        # Create Plotly Gantt chart
        fig = px.timeline(
            gantt_data,
            x_start="Start",
            x_end="Finish",
            y="Task",
            title=f"Diagramme de Gantt - {algorithm}",
            labels={"Task": "Tâches"},
        )
        fig.update_yaxes(categoryorder="total ascending")

        # Convert to HTML and return
        gantt_html = pio.to_html(fig, full_html=False)

        return jsonify({
            'result': result,
            'gantt_html': gantt_html
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
