classdef Position
    %Position and heading of a vehicle in coordinates for the HMI.
    
    properties
        Xpos
        Ypos
        Heading
    end
    
    methods
        function obj = Position(x_pos, y_pos, heading)
            %Constructor
            obj.Xpos = x_pos;
            obj.Ypos = y_pos;
            obj.Heading = heading;
        end
    end
end

