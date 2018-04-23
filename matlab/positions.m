function [rel_pos, rel_dir] = positions(pos_x, pos_y, dir, self_pos_x, self_pos_y, self_dir)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
rotation_matrix =   [cosd(-self_dir), sind(-self_dir);
                    sind(-self_dir), -cosd(-self_dir)];

rel_pos = rotation_matrix * [(pos_x - self_pos_x); (pos_y - self_pos_y)] + [self_pos_x; self_pos_y];

rel_dir = dir - self_dir;
end

