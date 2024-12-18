import heapq

# 1. **FCFS (First Come, First Served)** :
def fcfs(tasks):
    """
    Planification FCFS (First Come, First Served).
    Entrée : Liste des tâches avec 'id', 'arrival_time', 'execution_time'.
    Sortie : Liste des temps de début et fin avec les étapes de l'algorithme.
    """
    tasks.sort(key=lambda x: x['arrival_time'])  # Trier par ordre d'arrivée
    schedule = []
    steps = []  # To track the steps
    current_time = 0
    
    for task in tasks:
        start_time = max(current_time, task['arrival_time'])
        end_time = start_time + task['execution_time']
        
        schedule.append({'task': task['id'], 'start': start_time, 'end': end_time})
        
        steps.append(f"At time {current_time}, task {task['id']} is ready (Arrival: {task['arrival_time']}).")
        steps.append(f"Task {task['id']} starts at {start_time} and ends at {end_time}.")
        
        current_time = end_time
    
    return schedule, steps



# 2. **SJF (Shortest Job First)** :
def sjf(tasks):
    """
    Planification SJF (Shortest Job First).
    Entrée : Liste des tâches avec 'id', 'arrival_time', 'execution_time'.
    Sortie : Liste des temps de début et fin avec les étapes de l'algorithme.
    """
    tasks.sort(key=lambda x: x['arrival_time'])  # Trier par ordre d'arrivée
    ready_queue = []  # Queue ready for tasks
    schedule = []
    steps = []  # To track the steps
    current_time = 0
    
    while tasks or ready_queue:
        while tasks and tasks[0]['arrival_time'] <= current_time:
            heapq.heappush(ready_queue, (tasks[0]['execution_time'], tasks.pop(0)))

        if ready_queue:
            execution_time, task = heapq.heappop(ready_queue)
            start_time = current_time
            end_time = start_time + execution_time
            
            schedule.append({'task': task['id'], 'start': start_time, 'end': end_time})
            
            steps.append(f"At time {current_time}, tasks {', '.join([str(t['id']) for t in tasks])} are waiting.")
            steps.append(f"Task {task['id']} with execution time {execution_time} selected for execution.")
            steps.append(f"Task {task['id']} starts at {start_time} and ends at {end_time}.")
            
            current_time = end_time
        else:
            current_time = tasks[0]['arrival_time']
    
    return schedule, steps


# 3. **RM (Rate Monotonic Scheduling)** :
def rm(tasks):
    """
    Planification RM (Rate Monotonic Scheduling).
    Entrée : Liste des tâches avec 'id', 'execution_time', 'period'.
    Sortie : Liste des temps de début et fin avec les étapes de l'algorithme.
    """
    tasks = sorted(tasks, key=lambda x: x['period'])  # Trier par période (priorité)
    schedule = []
    steps = []  # To track the steps
    current_time = 0
    
    for _ in range(10):  # Looping through tasks for several periods
        for task in tasks:
            start_time = current_time
            end_time = start_time + task['execution_time']
            
            schedule.append({'task': task['id'], 'start': start_time, 'end': end_time})
            
            steps.append(f"At time {current_time}, task {task['id']} is ready (Period: {task['period']}).")
            steps.append(f"Task {task['id']} starts at {start_time} and ends at {end_time}.")
            
            current_time = end_time
    
    return schedule, steps



# 4. **DM (Deadline Monotonic Scheduling)** :
def dm(tasks):
    """
    Planification DM (Deadline Monotonic Scheduling).
    Entrée : Liste des tâches avec 'id', 'execution_time', 'deadline'.
    Sortie : Liste des temps de début et fin avec les étapes de l'algorithme.
    """
    tasks.sort(key=lambda x: x['deadline'])  # Trier par deadline
    schedule = []
    steps = []  # To track the steps
    current_time = 0
    
    for task in tasks:
        start_time = max(current_time, task['arrival_time'])
        end_time = start_time + task['execution_time']
        
        schedule.append({'task': task['id'], 'start': start_time, 'end': end_time})
        
        steps.append(f"At time {current_time}, task {task['id']} is ready (Deadline: {task['deadline']}).")
        steps.append(f"Task {task['id']} starts at {start_time} and ends at {end_time}.")
        
        current_time = end_time
    
    return schedule, steps



# 5. **LLF (Least Laxity First)** :
def llf(tasks):
    """
    Planification LLF (Least Laxity First).
    Entrée : Liste des tâches avec 'id', 'execution_time', 'deadline', 'arrival_time'.
    Sortie : Liste des temps de début et fin avec les étapes de l'algorithme.
    """
    schedule = []
    steps = []  # To track the steps
    current_time = 0
    
    while tasks:
        for task in tasks:
            task['laxity'] = task['deadline'] - (current_time + task['execution_time'])
        
        steps.append(f"At time {current_time}, calculating laxities: " +
                     ", ".join([f"Task {task['id']} (Laxity: {task['laxity']})" for task in tasks]))
        
        tasks.sort(key=lambda x: x['laxity'])  # Sort tasks by laxity
        
        task = tasks.pop(0)  # Select the task with the least laxity
        
        steps.append(f"Selected Task {task['id']} for execution (Laxity: {task['laxity']})")
        
        start_time = current_time
        end_time = start_time + task['execution_time']
        
        schedule.append({'task': task['id'], 'start': start_time, 'end': end_time})
        
        current_time = end_time
        
        steps.append(f"Task {task['id']} starts at {start_time} and ends at {end_time}.")
    
    return schedule, steps



# 6. **EDF (Earliest Deadline First)** :
def edf(tasks):
    """
    Planification EDF (Earliest Deadline First).
    Entrée : Liste des tâches avec 'id', 'execution_time', 'deadline', 'arrival_time'.
    Sortie : Liste des temps de début et fin avec les étapes de l'algorithme.
    """
    schedule = []
    steps = []  # To track the steps
    current_time = 0
    
    while tasks:
        tasks.sort(key=lambda x: x['deadline'])  # Sort tasks by deadline
        
        task = tasks.pop(0)
        
        start_time = max(current_time, task['arrival_time'])
        end_time = start_time + task['execution_time']
        
        schedule.append({'task': task['id'], 'start': start_time, 'end': end_time})
        
        steps.append(f"At time {current_time}, task {task['id']} is ready (Deadline: {task['deadline']}).")
        steps.append(f"Task {task['id']} starts at {start_time} and ends at {end_time}.")
        
        current_time = end_time
    
    return schedule, steps



# 7. **SJF Preemptive (Shortest Job First - Preemptive)** :
def sjf_preemptive(tasks):
    """
    Planification SJF Preemptive (Shortest Job First - Preemptive).
    Entrée : Liste des tâches avec 'id', 'arrival_time', 'execution_time'.
    Sortie : Liste avec les temps de début et fin pour chaque tâche.
    """
    tasks.sort(key=lambda x: x['arrival_time'])
    ready_queue = []
    current_time = 0
    schedule = []
    remaining_tasks = {task['id']: task['execution_time'] for task in tasks}

    while tasks or ready_queue:
        while tasks and tasks[0]['arrival_time'] <= current_time:
            heapq.heappush(ready_queue, (tasks[0]['execution_time'], tasks.pop(0)))

        if ready_queue:
            execution_time, task = heapq.heappop(ready_queue)
            start_time = current_time
            # Execute the task for 1 unit of time
            current_time += 1
            remaining_tasks[task['id']] -= 1

            if remaining_tasks[task['id']] > 0:
                heapq.heappush(ready_queue, (remaining_tasks[task['id']], task))

            end_time = start_time + 1
            schedule.append({'task': task['id'], 'start': start_time, 'end': end_time})
        else:
            current_time = tasks[0]['arrival_time']
    return schedule


# Exemple d'utilisation
if __name__ == "__main__":
    example_tasks = [
        {"id": 1, "arrival_time": 0, "execution_time": 3, "deadline": 7, "period": 10},
        {"id": 2, "arrival_time": 2, "execution_time": 6, "deadline": 8, "period": 15},
        {"id": 3, "arrival_time": 4, "execution_time": 4, "deadline": 10, "period": 20},
    ]

    print("FCFS :", fcfs(example_tasks.copy()))
    print("SJF :", sjf(example_tasks.copy()))
    print("SJF Preemptive:", sjf_preemptive(example_tasks.copy()))
    print("RM :", rm(example_tasks.copy()))
    print("DM :", dm(example_tasks.copy()))
    print("LLF :", llf(example_tasks.copy()))
    print("EDF :", edf(example_tasks.copy()))
