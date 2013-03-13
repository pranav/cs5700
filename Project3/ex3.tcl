if {[llength $argv] != 2} {
    puts "Missing parameter: queuetype, tracefile"
    exit 1
}

set queuetype [lindex $argv 0]
set tfname [lindex $argv 1]

#Create a simulator object
set ns [new Simulator]

set tf [open $tfname w]
$ns trace-all $tf


#Define a 'finish' procedure
proc finish {} {
        global ns tf
        $ns flush-trace

        close $tf
        exit 0
}

# Create nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

# Create links between the nodes
$ns duplex-link $n1 $n2 10Mb 10ms $queuetype
$ns duplex-link $n2 $n5 10Mb 10ms $queuetype
$ns duplex-link $n2 $n3 10Mb 10ms $queuetype
$ns duplex-link $n3 $n4 10Mb 10ms $queuetype
$ns duplex-link $n3 $n6 10Mb 10ms $queuetype

# Give node position for NAM
$ns duplex-link-op $n1 $n2 orient right-down
$ns duplex-link-op $n5 $n2 orient right-up
$ns duplex-link-op $n2 $n3 orient right
$ns duplex-link-op $n3 $n4 orient right-up
$ns duplex-link-op $n3 $n6 orient right-down

$ns duplex-link-op $n2 $n3 queuePos 0.5

# Connect Node 1 and Node 4 with a TCP stream

set tcp1 [new Agent/TCP/Reno]
$ns attach-agent $n1 $tcp1

set sink4 [new Agent/TCPSink/Sack1]
$ns attach-agent $n4 $sink4

$ns connect $tcp1 $sink4

set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1
$ftp1 set type FTP

# Connect Node 5 and Node 6 with a UDP/CBR flow

set udp5 [new Agent/UDP]
$ns attach-agent $n5 $udp5

set sink6 [new Agent/Null]
$ns attach-agent $n6 $sink6

$ns connect $udp5 $sink6


# Set up CBR and attach to $udp5

set cbr5 [new Application/Traffic/CBR]
$cbr5 set interval_ 0.005
$cbr5 set type_ CBR
$cbr5 set packet_size_ 1000
$cbr5 set rate_ 10mb 
$cbr5 set random_ false

$cbr5 attach-agent $udp5


# set tcp [new Agent/TCP/{Reno, Newreno, Vegas}]  #for others

# Schedule events for the CBR and FTP agents
$ns at 0.05 "$ftp1 start"
$ns at 5.15 "$cbr5 start"

$ns at 15.05 "$ftp1 stop"
$ns at 15.05 "$cbr5 stop"


# Call the finish procedure after 5 seconds of simulation time
$ns at 15.10 "finish"

# Print CBR packet size and interval
# puts "CBR packet size = [$cbr2 set packet_size_]"
# puts "CBR interval = [$cbr2 set interval_]"

# Run the simulation
$ns run

close $tf
