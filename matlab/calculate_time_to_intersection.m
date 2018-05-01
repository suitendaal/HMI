function [vehicles, t_min, t_max] = calculate_time_to_intersection(vehicles, min_speed, max_acc)
    vehicle = {vehicles{1,1}, vehicles{1,2}};

%% Calculate time t_min to intersection with minimum speed 
    % t_min = 2 * vehicle.Dynamics.DisToInter / (min_speed + vehicle.Dynamics.Velocity
    t_min = 2 * vehicle{1}(8) / (min_speed + vehicle{1}(7));
    
%% Calculate time t_max to intersection with maximum acceleration
    % t_max = max(roots[max_acc/2, vehicle.Dynamics.Velocity,
    % -vehicle.Dynamics.DisToInter]))
    t_max = abs(max(roots([max_acc/2, vehicle{1}(7), -vehicle{1}(8)])));
    
%% Calculate predicted time to intersection
    vehicle{2} = zeros(1,3);
    % vehicle.TimeToInter = max(roots([vehicle.Dynamics.Acc/2,
    % vehicle.Dynamics.Velocity, -vehicle.Dynamics.DisToInter]))
    vehicle{2}(1) = max(roots([vehicle{1}(10)/2, vehicle{1}(7), -vehicle{1}(8)]));
    % speed_at_inter = vehicle.Dynamics.Velocity + vehicle.Dynamics.Acc * vehicle.TimeToInter;
    speed_at_inter = vehicle{1}(7) + vehicle{1}(10) * vehicle{2}(1);
    % vehicle.TimeToInterFront = vehicle.TimeToInter - vehicle.Type.CarLength / speed_at_inter;
    vehicle{2}(2) = vehicle{2}(1) - vehicle{1}(3) / speed_at_inter;
    % vehicle.TimeToInterBack = vehicle.TimeToInter + vehicle.Type.CarLength / speed_at_inter;
    vehicle{2}(3) = vehicle{2}(1) + vehicle{1}(3) / speed_at_inter;
    
    % KUTSIMULINK
    vehicles{1,1} = vehicle{1};
    vehicles{1,2} = vehicle{2};
end