from docplex.mp.model import Model
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.objects import *



def solve_open_shop(instance, max_time=1000, time_limit=100, threads=1):
    model = Model('OpenShop')
    start_time = dict()
    bigm = max_time

    # Define start time variables
    for task in instance.tasks:
        start_time[task] = model.continuous_var(name=f"start_{task.name}")

    # Prevent tasks on the same machine from overlapping
    for machine in instance.machines:
        for t1 in machine.tasks:
            for t2 in machine.tasks:
                if t1.name != t2.name:
                    prec = model.binary_var(name=f"{t1.name}_precedes_{t2.name}")
                    model.add(start_time[t1] + t1.length - bigm * (1 - prec) <= start_time[t2])
                    model.add(start_time[t2] + t2.length - bigm * prec <= start_time[t1])

    # Prevent tasks of the same job from overlapping (in any order)
    for job in instance.jobs:
        for t1 in job.tasks:
            for t2 in job.tasks:
                if t1.name != t2.name:
                    prec = model.binary_var(name=f"{t1.name}_precedes_{t2.name}_job")
                    model.add(start_time[t1] + t1.length - bigm * (1 - prec) <= start_time[t2])
                    model.add(start_time[t2] + t2.length - bigm * prec <= start_time[t1])

    # Minimize the makespan
    obj_var = model.continuous_var(0, max_time, 'makespan')
    for task in instance.tasks:
        model.add(obj_var >= start_time[task] + task.length)
    model.minimize(obj_var)


    # Define solver and solve
    model.parameters.timelimit.set(time_limit)
    model.parameters.threads.set(threads)
    sol = model.solve(log_output = True)
    
    solution = Solution(instance)

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
                print(task.name)
                results_file.write(f'{task.name}\n')
                start = sol.get_value(start_time[task])
                end = start + task.length
                print('Start: %f' % start)
                print('End: %f' % end)
                results_file.write(f'Start: {start:.6f}\n')
                results_file.write(f'End: {end:.6f}\n')
                solution.add(task, start, end)
        # Print and write the optimum result

        optimum_result = sol.get_objective_value()
        print('Optimum Result: %f' % optimum_result)
        results_file.write(f'Optimum Result: {optimum_result:.6f}\n')

    return solution



def optimize_and_visualize(time_limit = 100, threads = 1):
    reader = MyReader(is_open_shop = True)
    instance = reader.get_instance()
    solution = solve_open_shop(instance, time_limit = time_limit, threads = threads)
    solution.visualize(time_factor = 8, time_grid = 50)
    
if __name__ == '__main__':
    optimize_and_visualize(time_limit=100, threads=1)