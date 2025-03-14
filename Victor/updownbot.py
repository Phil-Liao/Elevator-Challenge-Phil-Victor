from api import Command, Simulation, UP, DOWN, MOVE, STOP


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
    while current_state["running"]:
        commands = []
        for elevator in current_state["elevators"]:
            # determine which direction to go
            direction = directions.get(elevator["id"], UP)
            if elevator["buttons_pressed"]:
                # go to the floor where the button is pressed inside the elevator
                destination_floor = elevator["buttons_pressed"][0]
                direction = UP if destination_floor > elevator["floor"] else DOWN
            else:
                # go to the requested floor directly
                for request in current_state["requests"]:
                    if request["floor"] != elevator["floor"]:
                        direction = UP if request["floor"] > elevator["floor"] else DOWN
                        break
            directions[elevator["id"]] = direction

            action = MOVE
            if elevator["floor"] in elevator["buttons_pressed"]:
                # let passengers off at this floor
                action = STOP
            else:
                for request in current_state["requests"]:
                    if request["floor"] == elevator["floor"] and request["direction"] == direction:
                        # someone requested the current floor
                        action = STOP
            commands.append(Command(elevator_id=elevator["id"], direction=direction, action=action))
            print(direction)
        current_state = simulation.send(commands)
    print("Score:", current_state.get("score"))
    print("Replay URL:", current_state.get("replay_url"))


if __name__ == "__main__":
    updown_bot()
