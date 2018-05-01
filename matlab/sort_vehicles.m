function sorted_vehicles = sort_vehicles(vehicles)
    time_to_inter = zeros(size(vehicles, 1));
    for i = 1:size(vehicles, 1)
        time_to_inter(i) = vehicles{i, 2}(1);
    end
    [~, ind] = sort(time_to_inter);
    
    sorted_vehicles = cell(size(vehicles, 1), 2);
    for i = 1:size(vehicles, 1)
        sorted_vehicles{i, 1} = vehicles{ind(i), 1};
        sorted_vehicles{i, 2} = vehicles{ind(i), 2};
    end
end

