function [vehicle_positions, environment_positions, advisory_speed] = main()

    receiver = sim('receiver_from_dSPACE');
    data = receiver.get('output_data');
    %data
    %vehicles = data(1);
    %environments = data(2);

    vehicle_positions = [];
    environment_positions = [];
    advisory_speed = 0;
end