from api import Command, Simulation, UP, DOWN, MOVE, STOP
from individual_nevigation import individual_nevigation

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
        print(requests)
        # assigning requests to elevators
        commands = []
        for elevator in current_state["elevators"]:
            # determine which direction to go
            direction = directions.get(elevator["id"], UP)
            stops = stopping_plan[elevator["id"]]["stops"]
            resting_floor = stopping_plan[elevator["id"]]["resting_floor"]
            directions[elevator["id"]] = direction

            if direction == UP and elevator["floor"] > stops[0]:
                direction = DOWN
            elif direction == DOWN and elevator["floor"] < stops[0]:
                direction = UP

            action = MOVE
            if elevator["floor"] == stops[0]:
                # let passengers off at this floor
                action = STOP
                stops.pop(0)
            else:
                pass
            commands.append(Command(elevator_id=elevator["id"], direction=direction, action=action))
        current_state = simulation.send(commands)
    print("Score:", current_state.get("score"))
    print("Replay URL:", current_state.get("replay_url"))


if __name__ == "__main__":
    updown_bot()
