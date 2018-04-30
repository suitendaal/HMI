function target_gap = find_target_gap(gaps)
%Function to find target gap
    target_gap = [];
    
    % Take the nearest gap which is large enough
    for i = 1:length(gaps)
        if gaps(i).IsGap && gaps(i).get_duration() > 1 * (main_vehicle.TimeToInterBack - main_vehicle.TimeToInterFront)
            target_gap = gaps(i);
            break
        end
    end
    
    % If no gap is found, take the largest gap
    if isempty(target_gap)
        duration = 0;
        index = 1;
        for i = 1:length(gaps)
            if gaps(i).get_duration() > duration
                duration = gaps(i).get_duration();
                index = i;
            end
        end
    end
    
    target_gap = gaps(index);
end

