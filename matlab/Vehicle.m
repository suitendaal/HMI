classdef Vehicle
    %UNTITLED Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        Type
        Pos_x
        Pos_y
        Direction
    end
    
    methods
        function obj = Vehicle(type, pos_x, pos_y, direction)
            % Vehicle constructor
            obj.Type = type;
            obj.Pos_x = pos_x;
            obj.Pos_y = pos_y;
            obj.Direction = direction;
        end
        
        function [pos, dir] = get_position(obj, self_pos_x, self_pos_y, self_dir)
            % Returns relative position from the main car
            [pos, dir] = positions(obj.Pos_x, obj.Pos_y, obj.Direction, self_pos_x, self_pos_y, self_dir);
        end
    end
    
    enumeration
        Car;
        Truck;
    end
end

