def assign_elevator(elevators, request):
    closest_elevator = None
    min_distance = float('inf')

    for elevator in elevators:
        if not elevator["buttons_pressed"]:  # Check if the elevator is not busy
            distance = abs(elevator["floor"] - request["floor"])
            if distance < min_distance:
                min_distance = distance
                closest_elevator = elevator

    return closest_elevator