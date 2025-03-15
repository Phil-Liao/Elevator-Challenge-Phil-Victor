def initial_stopping_plan(num_floors: int, elevator_data: list) -> dict:
    """
    Determine the initial stopping plan of the elevators

    Keyword Arguments:
    num_floors: total floors of the building
    elevator_data: current_state["elevators]
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


test_data = initial_stopping_plan(
    10,
    [
        {"buttons_pressed": [2, 3], "floor": 1, "id": "elevator-0"},
        {"buttons_pressed": [], "floor": 6, "id": "elevator-1"},
        {"buttons_pressed": [], "floor": 6, "id": "elevator-2"},
    ],
)
print(test_data)
