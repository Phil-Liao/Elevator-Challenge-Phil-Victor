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

    # Calculate the initial positions to equally space the elevators
    num_elevators = len(current_state["elevators"])
    num_floors = simulation.num_floors
    spacing = num_floors / (num_elevators + 2)

    
    for i, elevator in enumerate(current_state["elevators"]):
        elevator["floor"] = int((2*(i+1)-1) * spacing)

    while current_state["running"]:
        commands = []
        print(current_state)
        for elevator in current_state["elevators"]:
            if elevator["buttons_pressed"]:
                #if min(elevator["buttons_pressed"])
        middle_floor = (num_floors + 1) // 2  # calculate the middle floor
        current_state = simulation.send(commands)
    print("Score:", current_state.get("score"))
    print("Replay URL:", current_state.get("replay_url"))


if __name__ == "__main__":
    updown_bot()