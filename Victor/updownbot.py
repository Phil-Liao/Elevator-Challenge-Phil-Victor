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
    initial_stopping_plan = initial_stopping_plan(num_floors, elevator_data)

    for elevator in current_state["elevators"]:
        stopping_plan[elevator["id"]] = {
            "stops": [],
            "resting_floor": initial_stopping_plan[elevator["id"]]["resting_floor"]
        }
    print(f"Stopping Plan: {stopping_plan}")

    while current_state["running"]:
        requests = current_state["requests"]
        print(f"Requests :{requests}")
        commands = []

        # assigning requests to elevators
        for request in requests:
            if request["floor"] in assigned_requests:
                continue
            closest_elevator = assign_elevator(current_state["elevators"], request)
            if closest_elevator:
                stops = stopping_plan[closest_elevator["id"]]["stops"]
                stopping_plan[closest_elevator["id"]]["stops"] = individual_nevigation(stops, request["floor"], closest_elevator["floor"])
                assigned_requests.append(request["floor"])
                print(f"Assigned floor {request['floor']} to elevator {closest_elevator['id']}")

        for elevator in current_state["elevators"]:
            # determine which direction to go
            direction = directions.get(elevator["id"], UP)
            stops = stopping_plan[elevator["id"]]["stops"]
            resting_floor = stopping_plan[elevator["id"]]["resting_floor"]
            directions[elevator["id"]] = direction

            action = MOVE  # Initialize action to MOVE by default

            print(elevator["buttons_pressed"])
            for button_pressed in elevator["buttons_pressed"]:
                if not (button_pressed in stops):
                    stops = individual_nevigation(stops, button_pressed, elevator["floor"])
            print(f"New stops: {stops}")

            if stops:
                # if there are stops planned
                if direction == UP and elevator["floor"] > stops[0]:
                    direction = DOWN
                elif direction == DOWN and elevator["floor"] < stops[0]:
                    direction = UP

                if elevator["floor"] == stops[0]:
                    # let passengers off at this floor
                    action = STOP
                    print(f"Stopping at floor {elevator['floor']}")
                    stops.remove(elevator["floor"])
                    # Change direction to match the passenger's request direction
                    for request in requests:
                        if request["floor"] == elevator["floor"]:
                            direction = request["direction"]
                            assigned_requests.remove(elevator["floor"])
                            break
            else:
                # if there are no stops assigned, go to the resting floor
                if elevator["floor"] > resting_floor:
                    direction = DOWN
                elif elevator["floor"] < resting_floor:
                    direction = UP
                else:
                    action = STOP

            commands.append(Command(elevator_id=elevator["id"], direction=direction, action=action))
        current_state = simulation.send(commands)
    print("Score:", current_state.get("score"))
    print("Replay URL:", current_state.get("replay_url"))

if __name__ == "__main__":
    updown_bot()