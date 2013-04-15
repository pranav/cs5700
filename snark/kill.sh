a=`ps | grep java | cut -d ' ' -f1`

kill -9 $a

