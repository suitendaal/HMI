function vehicles = vehicle_convert(number_of_vehicles, vehicle_data)
    vehicles = cell(number_of_vehicles, 2);
    for i = 1:number_of_vehicles
        vehicles{i, 1} = zeros(1, 10);
        vehicles{i, 2} = zeros(1, 3);
    end
    
    % Define main vehicle
    current_vehicle = vehicle_data(1:10);
        
    part_nr = current_vehicle(1);
    type = [current_vehicle(2), current_vehicle(3)];
    position = [current_vehicle(4), current_vehicle(5), current_vehicle(6)];
    dynamics = [current_vehicle(7), current_vehicle(8), current_vehicle(9), current_vehicle(10)];
    
    vehicles{1, 1} = [part_nr, type, position, dynamics];
    vehicles{1, 2} = zeros(1,3);
    
    % Define other vehicles
    index = 2;
    for i = 11:9:length(vehicle_data)
        current_vehicle = vehicle_data(i:i+8);
        
        part_nr = current_vehicle(1);
        type = [current_vehicle(2), current_vehicle(3)];
        position = [current_vehicle(4), current_vehicle(5), current_vehicle(6)];
        dynamics = [current_vehicle(7), current_vehicle(8), current_vehicle(9)];
    
        vehicles{index, 1} = [part_nr, type, position, dynamics];
        vehicles{index, 2} = zeros(1,3);
        index = index + 1;
    end
end
