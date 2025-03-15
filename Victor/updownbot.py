from api import Command, Simulation, UP, DOWN, MOVE, STOP
from individual_nevigation import individual_nevigation
from assign_elevator import assign_elevator
from initial_stopping_plan import initial_stopping_plan

def updown_bot():
    """An example bot that sends elevators up and down and stops at floors if there are passengers waiting to get on or off"""
    simulation = Simulation(
        event="secondspace2025",
        building_name="medium_random",
        bot="phil-and-victor-bot",
        email="victorhsiao5@gmail.com",
        sandbox=True,
    )
    current_state = simulation.initial_state
    directions = {}  # current directions of elevators
    stopping_plan = {}  # floors where the elevator should stop
    assigned_requests = []
    num_floors = simulation.num_floors
    elevator_data = current_state["elevators"]
    initial_plan = initial_stopping_plan(num_floors, elevator_data)  # Changed variable name here

    # Debug print for initial setup
    print(f"Number of floors: {num_floors}")
    print(f"Initial elevator data: {elevator_data}")

    for elevator in current_state["elevators"]:
        stopping_plan[elevator["id"]] = {
            "stops": [],
            "resting_floor": initial_plan[elevator["id"]]["resting_floor"]  # Updated reference here
        }
    print(f"Initial Stopping Plan: {stopping_plan}")

    while current_state["running"]:
        requests = current_state["requests"]
        print(f"\n=== New Turn ===")
        print(f"Current Requests: {requests}")
        print(f"Currently Assigned Requests: {assigned_requests}")
        commands = []

        # First, handle new requests
        for request in requests:
            if request["floor"] not in assigned_requests:  # Check if request is unassigned
                closest_elevator = assign_elevator(current_state["elevators"], request)
                if closest_elevator:
                    stops = stopping_plan[closest_elevator["id"]]["stops"]
                    new_stops = individual_nevigation(stops, request["floor"], closest_elevator["floor"])
                    stopping_plan[closest_elevator["id"]]["stops"] = new_stops
                    assigned_requests.append(request["floor"])
                    print(f"DEBUG: Assigned pickup at floor {request['floor']} to elevator {closest_elevator['id']}")
                    print(f"DEBUG: Updated stops list: {new_stops}")

        # Then process each elevator
        for elevator in current_state["elevators"]:
            direction = directions.get(elevator["id"], UP)
            stops = stopping_plan[elevator["id"]]["stops"]
            resting_floor = stopping_plan[elevator["id"]]["resting_floor"]
            
            print(f"\nDEBUG: Processing elevator {elevator['id']}:")
            print(f"DEBUG: Current floor: {elevator['floor']}, Current stops: {stops}")
            
            action = MOVE  # Initialize action to MOVE by default

            # Handle button presses first
            if elevator["buttons_pressed"]:
                for button_pressed in elevator["buttons_pressed"]:
                    if button_pressed not in stops:
                        print(f"DEBUG: Adding button press {button_pressed} to stops")
                        new_stops = individual_nevigation(stops, button_pressed, elevator["floor"])
                        stopping_plan[elevator["id"]]["stops"] = new_stops
                        stops = new_stops
                        print(f"DEBUG: Updated stops after button press: {stops}")

            # Check if we need to pick up any waiting passengers at current floor
            for request in requests:
                if request["floor"] == elevator["floor"] and request["floor"] not in assigned_requests:
                    action = STOP
                    print(f"DEBUG: Stopping to pick up passenger at floor {elevator['floor']}")
                    assigned_requests.append(request["floor"])

            if stops:
                next_stop = stops[0]
                if elevator["floor"] < next_stop:
                    direction = UP
                elif elevator["floor"] > next_stop:
                    direction = DOWN

                if elevator["floor"] == next_stop:
                    action = STOP
                    print(f"DEBUG: Stopping at floor {elevator['floor']}")
                    try:
                        stops.remove(elevator["floor"])
                        stopping_plan[elevator["id"]]["stops"] = stops
                        print(f"DEBUG: Removed floor {elevator['floor']} from stops")
                        if elevator["floor"] in assigned_requests:
                            assigned_requests.remove(elevator["floor"])
                    except ValueError:
                        print(f"DEBUG: Floor {elevator['floor']} not found in stops list")

            else:
                # Return to resting floor if no stops
                if elevator["floor"] != resting_floor:
                    direction = UP if elevator["floor"] < resting_floor else DOWN
                else:
                    action = STOP

            directions[elevator["id"]] = direction
            commands.append(Command(elevator_id=elevator["id"], direction=direction, action=action))
            print(f"DEBUG: Final command - floor: {elevator['floor']}, direction: {direction}, action: {action}")

        current_state = simulation.send(commands)
        
    print("Score:", current_state.get("score"))
    print("Replay URL:", current_state.get("replay_url"))

if __name__ == "__main__":
    updown_bot()