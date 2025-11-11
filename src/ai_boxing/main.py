#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from ai_boxing.crew import AiBoxing

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    # Prompt user for required inputs
    boxer_name = input("Enter the name of the boxer: ")
    country_code = input("Enter your country code (e.g., 33 for France): ")
    phone_number = input("Enter your phone number (without country code): ")

    # Add any other required variables here

    inputs = {
        "boxer_name": boxer_name,
        "country_code": country_code,
        "phone_number": phone_number,
        'topic': 'boxing',
        'current_year': str(datetime.now().year),
        'current_month': str(datetime.now().month)
        # Add other variables as needed
    }
    try:
        AiBoxing().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
     # Prompt user for required inputs
    boxer_name = input("Enter the name of the boxer: ")
    country_code = input("Enter your country code (e.g., 33 for France): ")
    phone_number = input("Enter your phone number (without country code): ")

    # Add any other required variables here

    inputs = {
        "boxer_name": boxer_name,
        "country_code": country_code,
        "phone_number": phone_number,
        'topic': 'boxing',
        'current_year': str(datetime.now().year)
        # Add other variables as needed
    }
    try:
        AiBoxing().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AiBoxing().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
   # Prompt user for required inputs
    boxer_name = "Gervonta Davis"
    country_code = "33"
    phone_number = "753862654"

    # Add any other required variables here

    inputs = {
        "boxer_name": boxer_name,
        "country_code": country_code,
        "phone_number": phone_number,
        'topic': 'boxing',
        'current_year': str(datetime.now().year)
        # Add other variables as needed
    }
    try:
        AiBoxing().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
