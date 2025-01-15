# SAAD - Open Shop and Job Shop Scheduling Problem using CPLEX

This project is a implementation of the Open Shop and Job Shop Scheduling Problem using CPLEX. The project was developed as a final project for the discipline of analytical decision support systems.

## Problem Description

The Open Shop and Job Shop Scheduling Problem are two well-known scheduling problems in the literature. The Job Shop scheduling problem aims to distribute a set of jobs with different operations on a set of machines. The operations should be run following an order. The Open Shop scheduling problem is similar, but the order of the operations is not fixed. 

The problems used in this project are based on [this](http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html) website. The data is extracted as needed to the 'data' folder.


## Setting Up the Environment

1. Install Anaconda or Miniconda from [here](https://www.anaconda.com/products/distribution).

2. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/project-name.git
   cd project-name

3. Create a new conda environment:
   ```bash
    conda env create -f environment.yml
    ```
4. Activate the environment:
    ```bash
    conda activate saad
    ```
5. Run the project using the following command:
    ```bash
    python main.py
    ```

## Solution Output

- After running the desired problem, the solution will be displayed in the terminal, and a graphical representation of the schedule will be stored on the 'solutions' folder.
