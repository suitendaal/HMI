function advisory_speed = calculate_advisory_speed(vehicles, t_max)

%% Devide client from HMI and other vehicles
    main_vehicle = {vehicles{1, 1}, vehicles{1, 2}};
    vehicles(1, :) = [];
    
%% Calculate time to reach intersection for other vehicles for front, middle and back
    for i = 1:size(vehicles, 1)
        vehicle = {vehicles{i, 1}, vehicles{i, 2}};
        % vehicle.TimeToInter = vehicle.Dynamics.DisToInter / vehicle.Dynamics.Velocity;
        vehicle{2}(1) = vehicle{1}(8) / vehicle{1}(7);
        % vehicle.TimeToInterFront = (vehicle.Dynamics.DisToInter - vehicle.Type.CarLength / 2) / vehicle.Dynamics.Velocity;
        vehicle{2}(2) = (vehicle{1}(8) - vehicle{1}(3) / 2) / vehicle{1}(7);
        % vehicle.TimeToInterBack = (vehicle.Dynamics.DisToInter + vehicle.Type.CarLength / 2) / vehicle.Dynamics.Velocity;
        vehicle{2}(3) = (vehicle{1}(8) + vehicle{1}(3) / 2) / vehicle{1}(7);
        vehicles{i,1} = vehicle{1};
        vehicles{i,2} = vehicle{2};
    end
    
%% Sort vehicles on time to inter in order from long to short
    vehicles = sort_vehicles(vehicles);
    
%% Delete vehicles which are not in the right lane
    index_to_delete = [];
    lane_id = zeros(size(vehicles, 1),1);
    
    for i = 1:size(vehicles, 1)
        lane_id(i) = vehicles{i, 1}(9);
    end
    
    for i = 1:size(vehicles, 1)
        % if vehicles(i).Dynamics.Lane ~= 0
        if ~isempty(vehicles{i}) 
            if lane_id(i) ~= 0
                index_to_delete = [index_to_delete, i];
            end
        end
    end
    vehicles(index_to_delete,:) = [];
    
%% Create an array with gaps

    % Define begin- and endtime of section and whether it is a gap or not
    gaps = cell(size(vehicles, 1), 3);
    
    % Define first no_gap
    % gaps(1) = Gap(vehicle(1).TimeToInterBack, vehicle(1).TimeToInterFront, false);
    no_gap = [vehicles{1, 2}(3), vehicles{1, 2}(2), false];
    
    for j = 1:3
        gaps{1, j} = no_gap(j);
    end
    
    index = 2;
    
    for i = 2:size(vehicles, 1)
        % gap = Gap(vehicle(i-1).TimeToInterFront, vehicle(i).TimeToInterBack, true);
        gap = [vehicles{i-1, 2}(2), vehicles{i, 2}(3), true];
        
        for j = 1:3
            gaps{index, j} = gap(j);
        end
        index = index + 1;
        
        % no_gap = Gap(vehicle(i).TimeToInterBack, vehicle(i).TimeToInterFront, false);
        no_gap = [vehicles{i, 2}(3), vehicles{i, 2}(2), false];
        
        for j = 1:3
            gaps{index, j} = no_gap(j);
        end
        
        index = index + 1;
    end
    
    if vehicles{end,2}(2) > t_max
        gap = [vehicles{end, 2}(2), t_max, true];
        for j = 1:3
            gaps{index, j} = gap(j);
        end
    end
    
%% Decide which gap is the best gap
    % Sort gaps on time from predicted time
    gaps = sort_gaps(gaps, main_vehicle);
    
    % Find the nearest gap with an optimal size
    target_gap = find_target_gap(gaps, main_vehicle);
    
    % Calculate desired speed at intersection
    % advisory_speed = 2 * main_vehicle.Dynamics.DisToInter / target_gap.get_time_to_inter() + main_vehicle.Dynamics.Velocity; 
    advisory_speed = 2 * main_vehicle{1}(8) / get_time_to_inter(target_gap) + main_vehicle{1}(7); 
    
    % From m/s to km/h
    advisory_speed = advisory_speed * 3.6;
    
    % Round to 5
    advisory_speed = round(advisory_speed / 5) * 5;
end

function time_to_inter = get_time_to_inter(gap)
    time_to_inter = (gap{1} + gap{2}) / 2;
end