classdef Type
    %CarType
    
    properties
        CarType
        CarLength
    end
    
    methods
        function obj = Type(car_type, car_length)
            % Constructor
            obj.CarType = car_type;
            obj.CarLength = car_length;
        end
    end
end

