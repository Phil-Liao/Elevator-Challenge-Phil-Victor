from api import Command, Simulation, UP, DOWN, MOVE, STOP

def individual_nevigation(stops, floors_assigned, current_floor, resting_floor):
    # only take on floors_assigned when the elevator is empty
    # OR the elevator will pass the floor and heading the same direction
    stops = sorted(stops)
    if not stops and (floors_assigned > (current_floor & floors_assigned[""]) or floors_assigned < (current_floor & floors_assigned)):
        print(f"the elevator cannnot accept the floor: {floors_assigned}")
    else:
        stops.append(floors_assigned)
        stops = sorted(stops)
        if current_floor < stops[0]:
            pass
        else:
            stops.reverse()
    return stops


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
    stopping_plan = {} # floors where the elevator should stop
    for elevator in current_state["elevators"]:
        stopping_plan[elevator["id"]] = []

    while current_state["running"]:
        requests = current_state["requests"]
        # assigning requests to elevators
        commands = []
        for elevator in current_state["elevators"]:
            # determine which direction to go
            direction = directions.get(elevator["id"], UP)
            if elevator["buttons_pressed"]:
                # go to the floor where the button is pressed inside the elevator
                direction = UP if destination_floor > elevator["floor"] else DOWN
            else:
                # go to the requested floor directly
                for request in current_state["requests"]:
                    request_tuple = (request["floor"], request["direction"])
                    if request_tuple not in assigned_requests and request["floor"] != elevator["floor"]:
                        direction = UP if request["floor"] > elevator["floor"] else DOWN
                        assigned_requests.add(request_tuple)
                        break
            directions[elevator["id"]] = direction

            action = MOVE
            if elevator["floor"] in elevator["buttons_pressed"]:
                # let passengers off at this floor
                action = STOP
            else:
                for request in current_state["requests"]:
                    if request["floor"] == elevator["floor"]:
                        # someone requested the current floor
                        action = STOP
                        assigned_requests.discard((request["floor"], request["direction"]))  # remove request from assigned
            commands.append(Command(elevator_id=elevator["id"], direction=direction, action=action))
            print(direction)
        current_state = simulation.send(commands)
    print("Score:", current_state.get("score"))
    print("Replay URL:", current_state.get("replay_url"))


if __name__ == "__main__":
    updown_bot()
