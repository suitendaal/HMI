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
        function [pos, dir] = get_position(self_pos_x, self_pos_y, self_dir)
            %UNTITLED Construct an instance of this class
            %   Detailed explanation goes here
            [pos, dir] = positions(Pos_x, Pos_y, Direction, self_pos_x, self_pos_y, self_dir)
        end
    end
end

