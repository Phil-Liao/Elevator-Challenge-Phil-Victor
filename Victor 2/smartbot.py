from api import Command, Simulation, UP, DOWN, MOVE, STOP

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

    
    # Assigning elevator
    requests = current_state["requests"]
    
    for request in requests:
        # calculating the distance between the request and the elevators and check for direction
        distance = {}
        for elevator in free_elevators:
            distance = request["floor"] - elevator["floor"]
            distance[elevator["id"]] = {"distance":distance, "direction":None}
        for elevator in up_elevators:
            distance = request["floor"] - elevator["floor"]
            distance[elevator["id"]] = {"distance":distance, "direction":UP}
        for elevator in down_elevators:
            distance = request["floor"] - elevator["floor"]
            distance[elevator["id"]] = {"distance":distance, "direction":DOWN}
