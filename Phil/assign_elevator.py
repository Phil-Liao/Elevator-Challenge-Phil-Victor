def assign_elevator(elevators: list, request: dict, num_floors: int) -> dict:
    num_elevators = len(elevators)
    sector_size = num_floors // num_elevators
    remaining_floors = num_floors % num_elevators
    
    closest_elevator = None
    min_distance = float('inf')
    
    for elevator in elevators:
        # Determine the sector for the elevator
        elevator_id = int(elevator["id"][-1])
        elevator_sector_start = elevator_id * sector_size
        elevator_sector_end = elevator_sector_start + sector_size
        
        # Include remaining floors in the last sector
        if elevator_id == num_elevators - 1:
            elevator_sector_end += remaining_floors
        
        # Check if the request is within the elevator's sector
        if elevator_sector_start <= request["floor"] < elevator_sector_end:
            distance = abs(elevator["floor"] - request["floor"])
            
            if not elevator["buttons_pressed"]:  # Elevator is idle
                if distance < min_distance:
                    min_distance = distance
                    closest_elevator = elevator
            else:
                # Check if the elevator is moving in the same direction as the request
                if (request["direction"] and elevator["floor"] <= request["floor"] <= elevator["buttons_pressed"][-1]) or \
                   (not request["direction"] and elevator["floor"] >= request["floor"] >= elevator["buttons_pressed"][0]):
                    if distance < min_distance:
                        min_distance = distance
                        closest_elevator = elevator

    return closest_elevator

def dynamic_scheduling(elevators: list, requests: list, num_floors: int) -> dict:
    assignments = {}
    
    for request in requests:
        assigned_elevator = assign_elevator(elevators, request, num_floors)
        if assigned_elevator:
            elevator_id = assigned_elevator["id"]
            if elevator_id not in assignments:
                assignments[elevator_id] = []
            assignments[elevator_id].append(request)
            
            # Update the elevator's state
            assigned_elevator["buttons_pressed"].append(request["floor"])
            assigned_elevator["buttons_pressed"].sort()
    
    return assignments