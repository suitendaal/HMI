classdef Gap
    %Gap which tells if between 2 times is a gap or not
    
    properties
        BeginTime
        EndTime
        IsGap
    end
    
    methods
        function obj = Gap(begin_time, end_time, is_gap)
            %Constructor
            obj.BeginTime = begin_time;
            obj.EndTime = end_time;
            obj.IsGap = is_gap;
        end
        
        function time = get_time_to_inter(obj)
            time = (obj.BeginTime + obj.EndTime) / 2;
        end
        
        function duration = get_duration(obj)
            duration = obj.BeginTime - obj.EndTime;
        end
    end
end

