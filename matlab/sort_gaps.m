function sorted_gaps = sort_gaps(gaps, vehicle)
    begin_times = zeros(size(gaps, 1));
    end_times = zeros(size(gaps, 1));
    for i = 1:size(gaps, 1)
        begin_times(i) = gaps{i, 1};
        end_times(i) = gaps{i, 2};
    end
    time = (begin_times + end_times) / 2 - vehicle{2}(1);
    [~, ind] = sort(time);
    
    sorted_gaps = cell(size(gaps));
    for i = 1:size(gaps, 1)
        for j = 1:3
            sorted_gaps{i, j} = gaps{ind(i), j};
        end
    end
end

