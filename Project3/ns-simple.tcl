#Create a simulator object
set ns [new Simulator]

set tf [open my_experimental_output.tr w]
$ns trace-all $tf

#Define different colors for data flows (for NAM)
$ns color 1 Blue
$ns color 2 Red

#Open the NAM trace file
set nf [open out.nam w]
$ns namtrace-all $nf

#Define a 'finish' procedure
proc finish {} {
        global ns nf
        $ns flush-trace
        #Close the NAM trace file
        close $nf
        #Execute NAM on the trace file
        exec nam out.nam &
        exit 0
}

#Create four nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

#Create links between the nodes
#
$ns duplex-link $n1 $n2 10Mb 10ms DropTail
$ns duplex-link $n2 $n5 10Mb 10ms DropTail
$ns duplex-link $n2 $n3 10Mb 10ms DropTail
$ns duplex-link $n3 $n4 10Mb 10ms DropTail
$ns duplex-link $n3 $n6 10Mb 10ms DropTail


#Set Queue Size of link (n2-n3) to 10
# $ns queue-limit $n2 $n3 10

#Give node position (for NAM)
# $ns duplex-link-op $n0 $n2 orient right-down
# $ns duplex-link-op $n1 $n2 orient right-up
# $ns duplex-link-op $n2 $n3 orient right

#Monitor the queue for link (n2-n3). (for NAM)
# $ns duplex-link-op $n2 $n3 queuePos 0.5


# Setup a TCP connection
set tcp1 [new Agent/TCP]
$ns attach-agent $n1 $tcp1

set tcp2 [new Agent/TCP]
$ns attach-agent $n2 $tcp2

set tcp3 [new Agent/TCP]
$ns attach-agent $n3 $tcp3

set tcp4 [new Agent/TCP]
$ns attach-agent $n4 $tcp4

set tcp5 [new Agent/TCP]
$ns attach-agent $n5 $tcp5

set tcp6 [new Agent/TCP]
$ns attach-agent $n6 $tcp6


# Set up CBR
set cbr2 [new Application/Traffic/CBR]
$cbr2 attach-agent $tcp2


# Set TCP Sinks
set sink1 [new Agent/TCPSink]
$ns attach-agent $n1

set sink2 [new Agent/TCPSink]
$ns attach-agent $n2

set sink3 [new Agent/TCPSink]
$ns attach-agent $n3

set sink4 [new Agent/TCPSink]
$ns attach-agent $n4

set sink5 [new Agent/TCPSink]
$ns attach-agent $n5

set sink6 [new Agent/TCPSink]
$ns attach-agent $n6

$ns connect $tcp2 $sink3




# set tcp [new Agent/TCP/{Reno, Newreno, Vegas}]  #for others



set sink [new Agent/TCPSink]
$ns attach-agent $n3 $sink
$ns connect $tcp $sink
$tcp set fid_ 1

#Setup a FTP over TCP connection
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP


#Setup a UDP connection
set udp [new Agent/UDP]
$ns attach-agent $n1 $udp
set null [new Agent/Null]
$ns attach-agent $n3 $null
$ns connect $udp $null
$udp set fid_ 2

#Setup a CBR over UDP connection
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set packet_size_ 1000
$cbr set rate_ 1mb
$cbr set random_ false


#Schedule events for the CBR and FTP agents
$ns at 0.1 "$cbr start"
$ns at 1.0 "$ftp start"
$ns at 4.0 "$ftp stop"
$ns at 4.5 "$cbr stop"

#Detach tcp and sink agents (not really necessary)
$ns at 4.5 "$ns detach-agent $n0 $tcp ; $ns detach-agent $n3 $sink"

#Call the finish procedure after 5 seconds of simulation time
$ns at 5.0 "finish"

#Print CBR packet size and interval
puts "CBR packet size = [$cbr set packet_size_]"
puts "CBR interval = [$cbr set interval_]"

#Run the simulation
$ns run


close $tf
