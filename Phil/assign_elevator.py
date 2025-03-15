def assign_elevator(elevators, request, directions):
    closest_elevator = None
    min_distance = float('inf')

    for elevator in elevators:
        
        distance = elevator["floor"] - request["floor"]
        direction = False if distance<0 else True
        if (abs(distance) < min_distance) and (directions.get(elevator["id"])==direction):
            min_distance = distance
            closest_elevator = elevator

    return closest_elevator