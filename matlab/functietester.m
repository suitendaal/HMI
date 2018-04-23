function [rel_pos, rel_dir] = functietester()

vehicles = [

%% Moet eigenlijk de simulink shit importeren
pos_x = 6;
pos_y = 1;
dir = 90;
self_pos_x = 0;
self_pos_y = 1;
self_dir = 45;

[rel_pos, rel_dir] = positions(pos_x, pos_y, dir, self_pos_x, self_pos_y, self_dir);


end