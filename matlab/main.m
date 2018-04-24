function [vehicle_positions, environment_positions, advisory_speed] = main()

    receiver = sim('receiver');
    data = receiver.get('simout');
    vehicles = data[1];
    environments = data[2];

    vehicle_positions = [];
    environment_positions = [];
    advisory_speed = 0;
end