from api import Command, Simulation, UP, DOWN, MOVE, STOP
from individual_navigation import individual_navigation
from assign_elevator import assign_elevator
from initial_stopping_plan import initial_stopping_plan

def updown_bot():
    """An example bot that sends elevators up and down and stops at floors if there are passengers waiting to get on or off"""
    simulation = Simulation(
        event="secondspace2025",
        building_name="tiny_random",
        bot="updown-python-bot",
        email="bob@mail.com",
        sandbox=True,
    )
    current_state = simulation.initial_state
    directions = {}  # current directions of elevators
    stopping_plan = initial_stopping_plan(current_state["num_floors"], current_state["elevators"])  # floors where the elevator should stop
    assigned_requests = []

    print(f"Stopping Plan: {stopping_plan}")

    while current_state["running"]:
        requests = current_state["requests"]
        print(f"Requests :{requests}")
        commands = []
        stops = []
        # assigning requests to elevators
        for request in requests:
            if request["floor"] in assigned_requests:
                continue
            closest_elevator = assign_elevator(current_state["elevators"], request)
            if closest_elevator:
                stopping_plan = individual_navigation(stopping_plan, closest_elevator["id"], request["floor"], closest_elevator["floor"])
                assigned_requests.append(request["floor"])
                print(f"Assigned floor {request['floor']} to elevator {closest_elevator['id']}")

        for elevator in current_state["elevators"]:
            # determine which direction to go
            direction = directions.get(elevator["id"], UP)
            stops = stopping_plan[elevator["id"]]["stops"]
            resting_floor = stopping_plan[elevator["id"]]["resting_floor"]
            directions[elevator["id"]] = direction
            print(f"direction={directions}")
            action = MOVE  # Initialize action to MOVE by default

            print(f"button pressed :{elevator['buttons_pressed']}")
            if elevator["buttons_pressed"]:
                for button_pressed in elevator["buttons_pressed"]:
                    if button_pressed not in stops:
                        stops.append(button_pressed)
                stopping_plan[elevator["id"]]["stops"] = sorted(stops)

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
                    stops.pop(0)  # Remove the first value from the stops list
                    # Change direction to match the passenger's request direction
                    for request in requests:
                        if request["floor"] == elevator["floor"]:
                            direction = request["direction"]
                            assigned_requests.remove(elevator["floor"])
                            break
                    # Ensure the elevator continues to the next stop after picking up a passenger
                    if stops:
                        next_stop = stops[0]
                        if elevator["floor"] < next_stop:
                            direction = UP
                        elif elevator["floor"] > next_stop:
                            direction = DOWN
            else:
                # if there are no stops assigned, go to the resting floor
                if elevator["floor"] > resting_floor:
                    direction = DOWN
                elif elevator["floor"] < resting_floor:
                    direction = UP
                else:
                    action = STOP

            stopping_plan[elevator["id"]]["stops"] = list(set(stopping_plan[elevator["id"]]["stops"]))
            stopping_plan[elevator["id"]]["stops"] = sorted(stopping_plan[elevator["id"]]["stops"])
            commands.append(Command(elevator_id=elevator["id"], direction=direction, action=action))
            print(f'*Elevator {elevator["id"]} :\nstops: {stops}\nbutton_pressed: {elevator["buttons_pressed"]}\nfloor: {elevator["floor"]}\naction: {action}\ndirection: {direction}')
        current_state = simulation.send(commands)
    print("Score:", current_state.get("score"))
    print("Replay URL:", current_state.get("replay_url"))

if __name__ == "__main__":
    updown_bot()