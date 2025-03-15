from api import Command, Simulation, UP, DOWN, MOVE, STOP
from requests_processing import requests_processing

def smartbot():
    """A smart bot that only move when there is a request"""
    simulation = Simulation(
        event="secondspace2025",
        building_name="medium_random",
        bot="phil-and-victor-smartbot",
        email="victorhsiao5@gmail.com",
        sandbox=True,
    )
    # initializations
    current_state = simulation.initial_state
    directions = {}
    elevator_data = current_state["elevators"]
    assigned_requests = []

    
    # Resting position for each elevator
    for elevator in current_state["elevators"]:
        stopping_plan[elevator["id"]] = {
            "stops": [],
            "resting_floor": initial_plan[elevator["id"]]["resting_floor"]  # Updated reference here
        }
    print(f"Initial Stopping Plan: {stopping_plan}")

    while current_state["running"]:
        # Request processing
        requests = current_state["requests"]
        for request in requests:
            if request["floor"] in assigned_requests:
                requests.remove(request)
        assignment = requests_processing(requests, elevator_data)
        
        # command processing
        commands = []
        # actions for elevators
        if assignment:
            action = MOVE

            for elevator in current_state["elevators"]:
                if elevator["id"] in assignment.values():
                    direction = UP if elevator["floor"] < assignment.values() else DOWN
                    
                    
    
    
    commands.append(Command(elevator_id=elevator["id"], direction=direction, action=action))
