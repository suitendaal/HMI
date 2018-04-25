classdef Dynamics
    %Variables which describe the dynamics and the position on the road.
    %For calculations.
    
    properties
        Velocity
        Acc
        DisToInter
        Lane  
    end
    
    methods
        function obj = Dynamics(velocity, acc, dis_to_inter, lane)
            %Constructor
            obj.Velocity = velocity;
            obj.Acc = acc;
            obj.DisToInter = dis_to_inter;
            obj.Lane = lane;
        end
    end
end

