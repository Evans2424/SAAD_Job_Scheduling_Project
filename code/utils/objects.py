import json
import os
import requests

#import math

class Instance:
    def __init__(self, name, jobs, machines):
        self.name = name
        self.machines = machines
        self.jobs = jobs
        self.tasks = []
        for job in self.jobs:
            for task in job.tasks:
                self.tasks.append(task)

class Machine:
    def __init__(self, id):
        self.id = id
        self.tasks = set()
    
    def add_task(self, task):
        self.tasks.add(task)

class Job:
    def __init__(self, id):
        self.id = id
        self.tasks = [] # tasks are in a given order
        
    def append_task(self, task):
        if len(self.tasks) > 0:
            self.tasks[-1].next_task = task
            task.prev_task = self.tasks[-1]
        self.tasks.append(task)
        task.job = self

class Task:
    def __init__(self, name, machine, length):
        self.name = name
        self.machine = machine
        self.machine.add_task(self)
        self.length = length
        self.job = None
        self.next_task = None
        self.prev_task = None
    
    def __str__(self):
        return self.name

class MyReader:
    def __init__(self,is_open_shop):
        self.optimum_value = None
        problem_type, problem_number = self.get_user_input(is_open_shop)
       
        self.data_scrabber(problem_type, is_open_shop)

        self.instance = self.read_instance(problem_type, problem_number)
        print('>>>>>>>>>> Successfully loaded instance "%s", problem "%s" - known optimum: %s' % (problem_type,problem_number, self.optimum_value))
        print('\n')
        print('\n')

    
    def get_user_input(self,is_open_shop):
        if is_open_shop:
            problem_types = {
                '4jobs_4machines': 'tai4_4',
                '5jobs_5machines': 'tai5_5',
                '7jobs_7machines': 'tai7_7',
                '10jobs_10machines': 'tai10_10',
                '15jobs_15machines': 'tai15_15',
                '20jobs_20machines': 'tai20_20'
            }
        else:
            problem_types = {
                '15jobs_15machines': 'tai15_15',
                '20jobs_15machines': 'tai20_15',
                '20jobs_20machines': 'tai20_20',
                '30jobs_15machines': 'tai30_15',
                '30jobs_20machines': 'tai30_20',
                '50jobs_15machines': 'tai50_15',
                '50jobs_20machines': 'tai50_20',
                '100jobs_20machines': 'tai100_20'
            }
        
        print("Select the type of problem you want to solve:")
        for i, key in enumerate(problem_types.keys()):
            print(f"{i + 1}. {key.replace('_', ' ')}")
        
        problem_choice = int(input("Enter the number corresponding to your choice: ")) - 1
        problem_type = list(problem_types.values())[problem_choice]
        
        problem_number = int(input("Enter a problem number between 0 and 9: "))
        
        return problem_type, problem_number
        

    def read_instance(self, problem_type, problem_number):
        # Make a path to open the file it should be data/problem_type/problem_number.txt
        path = f'data/{problem_type}/{problem_number}.txt'

        jobs = []
        job_counter = 0

        # Open the file
        with open(path, 'r') as f:
            lines = f.readlines()
            
          
            second_line = lines[1].strip().split()
            number_jobs = int(second_line[0])
            number_machines = int(second_line[1])
            self.optimum_value = int(second_line[4])
            
            machines= [Machine(id = i) for i in range(number_machines)]

            reading_processing_times = True
            processing_times = []
            machine_assignments = []

            for line in lines[3:]:
                    if ('machines' in line) or ('Machines' in line):
                        reading_processing_times = False
                        continue
                    
                    if reading_processing_times:
                        if line.strip():  # Check if the line is not empty
                            processing_times.append(list(map(int, line.strip().split())))
                    else:
                        if line.strip():  # Check if the line is not empty
                            machine_assignments.append(list(map(int, line.strip().split())))
            
            print(processing_times)
            print(machine_assignments)

              # Create jobs and tasks
            for job_id in range(number_jobs):
                job = Job(job_id + 1)
                jobs.append(job)
                for task_id in range(number_machines):
                    name = f'j_{job_id + 1}_t_{task_id + 1}'
                
                    task_machine_id = machine_assignments[job_id][task_id]
                   
                    task_machine = machines[task_machine_id - 1]
                    
                    task_length = processing_times[job_id][task_id]
                
                    task = Task(name, task_machine, task_length)
                    job.append_task(task)
            
            


        instance_name = path.split('/')[-1].split('\\')[-1]


        return Instance(instance_name, jobs, machines)
            


    
    
    def data_scrabber(self, problem_type, is_open_shop):
        if is_open_shop:
            url = f'http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/openshop.dir/{problem_type}.txt'
        else:
            url = f'http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/jobshop.dir/{problem_type}.txt'

        response = requests.get(url)
        if response.status_code != 200:
            print('Could not fetch the problem specification from the URL.')
            raise SystemExit(0)
        
        # Create the data/tai4_4 directory if it doesn't exist
        directory = f'data/{problem_type}'
        if not os.path.exists(directory):
            os.makedirs(directory)

        lines = response.text.split('\n')
        sub_problem = []
        sub_problem_counter = 0
            
        for line in lines:
            if line.startswith('number') or line.startswith('Nb'):
                if sub_problem:
                    # Write the current sub_problem to a file
                    with open(f'{directory}/{sub_problem_counter}.txt', 'w') as f:
                        f.write('\n'.join(sub_problem))
                    sub_problem_counter += 1
                    sub_problem = []
            sub_problem.append(line.strip())
        
        # Write the last sub_problem to a file
        if sub_problem:
            with open(f'{directory}/{sub_problem_counter}.txt', 'w') as f:
                f.write('\n'.join(sub_problem))  

    def get_instance(self):
        return self.instance

class Solution:
    def __init__(self, instance):
        self.instance = instance
        self.solution = dict()
        self.tasks = list()
        
    def add(self, task, start, end):
        self.solution[task] = (start, end)
        self.tasks.append(task)
        
    def get_start_time(self, task):
        return self.solution[task][0]
        
    def get_end_time(self, task):
        return self.solution[task][1]
        
    def get_makespan(self):
        return max([self.get_end_time(task) for task in self.tasks])
        
    def visualize(self, path='solutions/solution.html', line_spacing=10, line_height=30, time_factor=5, time_grid=10):
        instance = self.instance

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)

        solution = self
        color_data = json.load(open(os.path.abspath(os.path.join(os.path.dirname(__file__), "%s" % 'colors.json')), 'r'))
        f = open(path, 'w')
        # first draw the machines
        for machine in instance.machines:
            f.write('<div style="position:absolute; left: 20px; top: %ipx; height: %ipx; width: %ipx; border-style: solid; border-width: 1px; border-color: black; text-align: center">M%i</div>\n' % (20 + (line_spacing + line_height) * machine.id, line_height, 30, machine.id))
        x_offset = 50
        # draw the time grid
        max_time = self.get_makespan()
        max_height = len(instance.machines) * (line_spacing + line_height) + line_height
        for t in range(time_grid, int(max_time + time_grid * 2), time_grid):
            f.write('<div style="position:absolute; left: %ipx; top: 0px; height: %ipx; width: 0px; border-style: solid; border-width: 0.5px; border-color: black"></div>\n' % (x_offset + t * time_factor, max_height))
            f.write('<div style="position:absolute; left: %ipx; top: %ipx; height: 20px; width: 50px; margin-left: -25px; border: 0; text-align: center">%i</div>\n' % (x_offset + t * time_factor, max_height + line_spacing, t))
        # then draw each task
        for task in instance.tasks:
            start = solution.get_start_time(task)
            end = solution.get_end_time(task)
            duration = end - start
            bg_color = color_data[str(len(instance.jobs))][task.job.id - 1][3]
            text_color = color_data[str(len(instance.jobs))][task.job.id - 1][4]
            f.write('<div style="position:absolute; left: %ipx; top: %ipx; height: %ipx; width: %ipx; border-style: solid; border-width: 1px; border-color: black; text-align: left; font-size: 8px; background-color: %s; color: %s"><div style="position: absolute; text-align: center; width: %ipx; margin: 0; top: 50%%; -ms-transform: translateY(-50%%); transform: translateY(-50%%)">%s</div></div>\n' % (x_offset + start * time_factor, 20 + (line_spacing + line_height) * task.machine.id, line_height, task.length * time_factor, bg_color, text_color, task.length * time_factor, task.name))
            if duration - task.length > 0:
                f.write('<div style="position:absolute; left: %ipx; top: %ipx; height: %ipx; width: %ipx; border-style: solid; border-width: 1px; border-color: black; text-align: left; font-size: 8px; background-color: %s; color: %s; background-image: radial-gradient(black 50%%, transparent 50%%); background-size: 2px 2px"></div>\n' % (x_offset + (start + task.length) * time_factor, 20 + (line_spacing + line_height) * task.machine.id + line_height / 4, line_height / 2, (duration - task.length) * time_factor, bg_color, text_color))
        f.write('<div style="position: absolute; left: 20px; top: %ipx"><u>Makespan:</u> %i</div>' % (max_height + 50, max_time))
        f.close()