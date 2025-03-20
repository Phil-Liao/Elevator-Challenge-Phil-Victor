from api import Command, Simulation, UP, DOWN, MOVE, STOP
from individual_navigation import individual_navigation
from assign_elevator import assign_elevator, dynamic_scheduling
from initial_stopping_plan import initial_stopping_plan, initial_stopping_plan_2

def updown_bot():
    """An example bot that sends elevators up and down and stops at floors if there are passengers waiting to get on or off"""
    simulation = Simulation(
        event="secondspace2025",
        building_name="big_random",
        bot="the_best_bot_by_Phil_and_Victor",
        email="cheweiphil@gmail.com",
        sandbox=False,
    )
    current_state = simulation.initial_state
    directions = {}  # current directions of elevators
    floors = current_state["num_floors"]
    stopping_plan = initial_stopping_plan(floors, current_state["elevators"])  # floors where the elevator should stop
    #stopping_plan = initial_stopping_plan(floors, current_state["elevators"])  # floors where the elevator should stop

    assigned_requests = []
    

    print(f"Stopping Plan: {stopping_plan}")

    while current_state["running"]:
        requests = current_state["requests"]
        print(f"Requests :{requests}")
        commands = []
        stops = []

        # Use dynamic scheduling to assign requests to elevators
        assignments = dynamic_scheduling(current_state["elevators"], requests, floors)
        
        for elevator_id, assigned_requests in assignments.items():
            for request in assigned_requests:
                stopping_plan = individual_navigation(stopping_plan, elevator_id, request["floor"], next(elevator for elevator in current_state["elevators"] if elevator["id"] == elevator_id)["floor"])
                print(f"Assigned floor {request['floor']} to elevator {elevator_id}")

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
                    stopping_plan = individual_navigation(stopping_plan, elevator["id"], button_pressed, elevator["floor"])

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
                            if elevator["floor"] in assigned_requests:
                                assigned_requests.remove(elevator["floor"])
                            break
                stopping_plan[elevator["id"]]["stops"] = list(set(stopping_plan[elevator["id"]]["stops"]))
                stopping_plan[elevator["id"]]["stops"].sort()
            else:
                # if there are no stops assigned, go to the resting floor
                if elevator["floor"] > resting_floor:
                    direction = DOWN
                elif elevator["floor"] < resting_floor:
                    direction = UP
                else:
                    action = STOP

            commands.append(Command(elevator_id=elevator["id"], direction=direction, action=action))
            print(f'*Elevator {elevator["id"]} :\nstops: {stops}\nbutton_pressed: {elevator["buttons_pressed"]}\nfloor: {elevator["floor"]}\naction: {action}\ndirection: {direction}')
        current_state = simulation.send(commands)
    print("Score:", current_state.get("score"))
    print("Replay URL:", current_state.get("replay_url"))

if __name__ == "__main__":
    while True:
        try:
            updown_bot()
            break
        except ConnectionError:
            print("error")