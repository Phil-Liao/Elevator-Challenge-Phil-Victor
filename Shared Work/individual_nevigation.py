def individual_nevigation(stops:list[int], floors_assigned:int, current_floor:int) -> list[list]:
    """
    Determine the individual navigation plan for an elevator.

    Args:
        stops (list[int]): A list of floors where the elevator needs to stop.
        floors_assigned (int): The floor that is assigned to the elevator.
        current_floor (int): The current floor of the elevator.
    """
    stops.append(floors_assigned)
    stops = sorted(stops)
    if current_floor < stops[0]:
        pass
    else:
        stops.reverse()
    return stops