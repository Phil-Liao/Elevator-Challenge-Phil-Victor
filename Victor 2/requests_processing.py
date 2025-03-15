def requests_processing(requests, elevator_data):
    # classifing elevators into: free, up, down
    free_elevators = []
    up_elevators = []
    down_elevators = []
    
    for elevator in elevator_data:
        if not elevator["buttons_pressed"]:
            free_elevators.append(elevator)
        elif elevator["direction"] == UP:
            up_elevators.append(elevator)
        elif elevator["direction"] == DOWN:
            down_elevators.append(elevator)
    
    # Assigning elevator
    assignments = {}
    for request in requests:
        # calculating the distance between the request and the elevators and check for direction
        request_elevators = {}
        for elevator in free_elevators:
            dist = abs(request["floor"] - elevator["floor"])  # Use abs() for absolute distance
            request_elevators[elevator["id"]] = {"distance": dist, "direction": None}
        for elevator in up_elevators:
            dist = abs(request["floor"] - elevator["floor"])
            request_elevators[elevator["id"]] = {"distance": dist, "direction": UP}
        for elevator in down_elevators:
            dist = abs(request["floor"] - elevator["floor"])
            request_elevators[elevator["id"]] = {"distance": dist, "direction": DOWN}

        # Sort elevators by distance
        sorted_elevators = dict(sorted(request_elevators.items(), 
                                     key=lambda x: x[1]["distance"]))
        
        # Check for multiple elevators with minimum distance
        min_distance = min(elevator_info["distance"] for elevator_info in request_elevators.values())
        closest_elevators = {
            elevator_id: info 
            for elevator_id, info in request_elevators.items() 
            if info["distance"] == min_distance
        }
        
        print(f"DEBUG: Elevators with minimum distance {min_distance}: {closest_elevators}")
        
        # If multiple elevators have the same minimum distance, prefer the one going in the same direction
        if len(closest_elevators) > 1:
            for elevator_id, info in closest_elevators.items():
                if info["direction"] == request["direction"]:
                    sorted_elevators = {elevator_id: info}  # Keep only this elevator
                    break
        
        # Return the closest elevator with None or the same direction
        for elevator_id, info in sorted_elevators.items():
            if info["direction"] is None or info["direction"] == request["direction"]:
                assignments[elevator_id] = request
                break
    return assignments


# Testing
UP, DOWN = True, False
test_requests = [
    {"floor": 5, "direction": UP},
    {"floor": 2, "direction": UP},
    {"floor": 7, "direction": DOWN},
]

test_elevators = [
    {"id": 1, "floor": 3, "direction": UP, "buttons_pressed": []},
    {"id": 2, "floor": 6, "direction": DOWN, "buttons_pressed": [3, 1]},
    {"id": 3, "floor": 4, "direction": UP, "buttons_pressed": [9]},
]

print(requests_processing(test_requests, test_elevators))