import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from docplex.cp.model import *
from utils.objects import *
    
def optimize(instance, max_time = 10000, time_limit = 100, threads = 1):
    model = CpoModel('BlockingJobShop')
    interval_vars = dict()
    
    # Create variables
    for task in instance.tasks:
        interval_vars[task] = interval_var(start = (0, max_time), end = (0, max_time), size = task.length, name = 'interval'+str(task.name))
    
    # Precedence and blocking constraints
    for task in instance.tasks:
        if task.next_task:
            model.add(start_of(interval_vars[task.next_task]) >= end_of(interval_vars[task]))
            
    # No overlap constraints
    for machine in instance.machines:
        machine_sequence = sequence_var([interval_vars[task] for task in machine.tasks])
        model.add(no_overlap(machine_sequence))
            
    # Minimize the makespan
    obj_var = integer_var(0, max_time, 'makespan')
    for task in instance.tasks:
        model.add(obj_var >= end_of(interval_vars[task]))
    model.minimize(obj_var)
    
    # Define solver and solve
    sol = model.solve(TimeLimit= time_limit, Workers = threads)
    
    solution = Solution(instance)
    
    # Define the path to the results file
    results_file_path = 'solutions/results.txt'

    # Ensure the solutions directory exists
    os.makedirs('solutions', exist_ok=True)

    # Delete the results file if it exists
    if os.path.exists(results_file_path):
        os.remove(results_file_path)

    # Open the results file for writing
    with open(results_file_path, 'w') as results_file:
        # Print out solution and return it
        for job in instance.jobs:
            for task in job.tasks:
                results_file.write(f'{task.name}\n')
                start = sol.get_value(interval_vars[task])[0]
                end = sol.get_value(interval_vars[task])[1]
                results_file.write(f'Start: {start:.6f}\n')
                results_file.write(f'End: {end:.6f}\n')
                solution.add(task, start, end)

    return solution
  


def optimize_and_visualize( time_limit = 100, threads = 1):
    reader = MyReader(is_open_shop=False)
    instance = reader.get_instance()
    solution = optimize(instance, time_limit = time_limit, threads = threads)
    solution.visualize(time_factor = 1, time_grid = 50)

if __name__ == '__main__':
    optimize_and_visualize()