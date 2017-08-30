 ps -ef | grep update_reg | awk '{print "kill -9 " $2}' | sh

