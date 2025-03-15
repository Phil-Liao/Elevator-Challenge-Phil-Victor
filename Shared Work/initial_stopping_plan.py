def initial_stopping_plan(num_floors: int, elevator_data: list) -> dict:
    """
    Determine the initial stopping plan of the elevators

    Keyword Arguments:
    num_floors: total floors of the building, current_state["num_floors"]
    elevator_data: current_state["elevators"]
    """
    elevators = len(elevator_data)
    spacing = num_floors / elevators
    stopping_plan = {}
    for i, elevator in enumerate(elevator_data):
        stopping_plan[elevator["id"]] = {
            "stops": [],
            "resting_floor": int((i + 0.5) * spacing),
        }

    return stopping_plan


