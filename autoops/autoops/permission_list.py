
from controller.controller_perm_logic import can_restart_node,can_start_node,can_stop_node
perm_dic={
    
    'can_restart_node':['table_list','GET',[],{},can_restart_node],
     'can_stop_node':['table_list','GET',[],{},can_stop_node],
    }