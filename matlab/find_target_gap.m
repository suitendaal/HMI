function target_gap = find_target_gap(gaps, vehicle)
%Function to find target gap
    target_gap = cell(1, 3);
    target_gap{1} = [];
    
    % Take the nearest gap which is large enough
    for i = 1:length(gaps)
        if gaps{i, 3} && get_duration(gaps{i, 1}, gaps{i, 2}) > 1 * (vehicle{2}(3) - vehicle{2}(2))
            for j = 1:3
                target_gap{j} = gaps{i, j};
            end
            break
        end
    end
    
    % If no gap is found, take the largest gap
    if isempty(target_gap{1})
        duration = 0;
        index = 1;
        for i = 1:size(gaps, 1)
            if get_duration(gaps{i, 1}, gaps{i, 2}) > duration
                duration = get_duration(gaps{i, 1}, gaps{i, 2});
                index = i;
            end
        end
        for j = 1:3
            target_gap{j} = gaps{index, j};
        end
    end
end

function duration = get_duration(begin_time, end_time)
    duration = abs(end_time - begin_time);
end