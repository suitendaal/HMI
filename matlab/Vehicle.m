classdef Vehicle
    %UNTITLED Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        % Id and characteristics
        PartNR
        Type
        
        % Position and speed
        Position
        Dynamics
        
        % Time to reach intersection
        TimeToInter
        TimeToInterFront
        TimeToInterBack
    end
    
    methods
        function obj = Vehicle(part_nr, type, position, dynamics)
            % Vehicle constructor
            obj.PartNR = part_nr;
            obj.Type = type;
            obj.Position = position;
            obj.Dynamics = dynamics;
        end
    end
end

