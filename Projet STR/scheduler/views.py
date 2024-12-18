from django.shortcuts import render
from django.http import JsonResponse
import json
from scheduling_algorithms import fcfs, sjf, rm, dm, llf, edf
import matplotlib.pyplot as plt
import os
from django.conf import settings

# Main page view
def index(request):
    return render(request, 'scheduler/index.html')

def generate_gantt_chart(schedule):
    """
    Generate a Gantt chart for the given schedule and save it to the media directory.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create a list of tasks and their start and end times for plotting
    tasks = [task['task'] for task in schedule]
    start_times = [task['start'] for task in schedule]
    end_times = [task['end'] for task in schedule]

    # Create a bar chart (Gantt chart)
    for i, (start, end) in enumerate(zip(start_times, end_times)):
        ax.barh(tasks[i], end - start, left=start, height=0.5, color='skyblue')

    ax.set_xlabel('Time')
    ax.set_ylabel('Tasks')
    ax.set_title('Gantt Chart for Task Scheduling')
    ax.grid(True)

    # Save the chart to a file in the media folder
    chart_filename = 'gantt_chart.png'
    chart_path = os.path.join(settings.MEDIA_ROOT, chart_filename)
    plt.savefig(chart_path)
    plt.close()

    # Return the relative URL to the saved image
    return os.path.join(settings.MEDIA_URL, chart_filename)


def simulate(request):
    if request.method == 'POST':
        algorithm = request.POST['algorithm']
        tasks_data = request.POST['tasks']
        tasks = json.loads(tasks_data)  # Safely convert the JSON string to Python object

        steps = []  # Initialize a list to hold the steps for display
        result = None  # Initialize the result variable
        
        # Select the appropriate algorithm and get the schedule and steps
        if algorithm == 'FCFS':
            result, steps = fcfs(tasks)
        elif algorithm == 'SJF':
            result, steps = sjf(tasks)
        elif algorithm == 'RM':
            result, steps = rm(tasks)
        elif algorithm == 'DM':
            result, steps = dm(tasks)
        elif algorithm == 'LLF':
            result, steps = llf(tasks)
        elif algorithm == 'EDF':
            result, steps = edf(tasks)

        # Format the schedule for display
        formatted_result = "\n".join([f"Task {task['task']} - Start: {task['start']}, End: {task['end']}" for task in result])

        # Format the steps for display
        formatted_steps = "\n".join(steps)

        # Generate Gantt chart and get the path to the saved image
        chart_path = generate_gantt_chart(result)

        return render(request, 'scheduler/simulate.html', {
            'result': formatted_result,
            'steps': formatted_steps,
            'gantt_chart': chart_path  # Pass the Gantt chart image path to the template
        })

    return render(request, 'scheduler/simulate.html')
