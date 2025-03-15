def assign_elevator(elevators: list, request: dict) -> dict:
    closest_elevator = None
    min_distance = float('inf')
    
    for elevator in elevators:
        if not elevator["buttons_pressed"]:  # Check if the elevator is not busy
            distance = abs(elevator["floor"] - request["floor"])
            if distance < min_distance:
                min_distance = distance
                closest_elevator = elevator
        else:
            # Check if the elevator is moving in the same direction as the request
            if request["direction"]:
                # Request is going up
                if elevator["floor"] <= request["floor"] and elevator["buttons_pressed"][-1] >= request["floor"]:
                    distance = abs(elevator["floor"] - request["floor"])
                    if distance < min_distance:
                        min_distance = distance
                        closest_elevator = elevator
            else:
                # Request is going down
                if elevator["floor"] >= request["floor"] and elevator["buttons_pressed"][-1] <= request["floor"]:
                    distance = abs(elevator["floor"] - request["floor"])
                    if distance < min_distance:
                        min_distance = distance
                        closest_elevator = elevator

    return closest_elevator