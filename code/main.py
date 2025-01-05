import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from open_shop_simple.open_shop_mip import optimize_and_visualize as open_shop_optimize_and_visualize
from job_shop_simple.simple_job_shop_mip import optimize_and_visualize as job_shop_optimize_and_visualize

if __name__ == '__main__':
    #Ask if the user wants to solve the job shop or the open shop problem
    print("Which problem would you like to solve?")
    print("1. Job Shop")
    print("2. Open Shop")
    problem = input("Enter 1 or 2: ")
    if problem == '1':
        job_shop_optimize_and_visualize()
    elif problem == '2':
        open_shop_optimize_and_visualize()
    else:
        print("Invalid input. Please enter 1 or 2")
        sys.exit(1)