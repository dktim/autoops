 ps -ef | grep uwsgi | awk '{print "kill -9 " $2}' | sh
 ps -ef | grep celery | awk '{print "kill -9 " $2}' | sh

