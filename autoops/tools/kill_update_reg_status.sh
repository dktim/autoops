ps -ef | grep update_reg_status | awk '{print "kill -9 " $2}' | sh

