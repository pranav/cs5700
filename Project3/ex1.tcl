if {[llength $argv] != 3} {
    puts "Missing parameter: cbr_bw, tracefile"
    exit 1
}

set bw [lindex $argv 0]
set tfname [lindex $argv 1]
set tcpv [lindex $argv 2]

#Create a simulator object
set ns [new Simulator]

set tf [open $tfname w]
$ns trace-all $tf

#Define different colors for data flows (for NAM)
$ns color 1 Blue
$ns color 2 Red

#Open the NAM trace file
#set nf [open out.nam w]
#$ns namtrace-all $nf

#Define a 'finish' procedure
proc finish {} {
        global ns tf
        $ns flush-trace
        #Close the NAM trace file
        close $tf
        #Execute NAM on the trace file
        #exec nam out.nam &
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
$ns duplex-link $n1 $n2 10Mb 10ms DropTail
$ns duplex-link $n2 $n5 10Mb 10ms DropTail
$ns duplex-link $n2 $n3 10Mb 10ms DropTail
$ns duplex-link $n3 $n4 10Mb 10ms DropTail
$ns duplex-link $n3 $n6 10Mb 10ms DropTail

# Give node position for NAM
$ns duplex-link-op $n1 $n2 orient right-down
$ns duplex-link-op $n5 $n2 orient right-up
$ns duplex-link-op $n2 $n3 orient right
$ns duplex-link-op $n3 $n4 orient right-up
$ns duplex-link-op $n3 $n6 orient right-down

$ns duplex-link-op $n2 $n3 queuePos 0.5

# Connect Node 1 and Node 4 with a TCP stream

set tcp1 [new Agent/$tcpv]
$ns attach-agent $n1 $tcp1
$tcp1 set class_ 2

set sink4 [new Agent/TCPSink]
$ns attach-agent $n4 $sink4
$sink4 set fid_ 1

$ns connect $tcp1 $sink4

set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1
$ftp1 set type FTP

# Connect N2 and N3

set udp2 [new Agent/UDP]
$ns attach-agent $n2 $udp2

set null3 [new Agent/Null]
$ns attach-agent $n3 $null3

$ns connect $udp2 $null3


# Set up CBR and attach to $udp2

set cbr2 [new Application/Traffic/CBR]
$cbr2 set interval_ 0.005
$cbr2 set type_ CBR
$cbr2 set packet_size_ 1000
$cbr2 set rate_ $bw
$cbr2 set random_ false

$cbr2 attach-agent $udp2


# set tcp [new Agent/TCP/{Reno, Newreno, Vegas}]  #for others

# Schedule events for the CBR and FTP agents
$ns at 0.05 "$ftp1 start"
$ns at 5.05 "$ftp1 stop"

#Detach tcp and sink agents (not really necessary)
# $ns at 4.5 "$ns detach-agent $n0 $tcp ; $ns detach-agent $n3 $sink"

#Call the finish procedure after 5 seconds of simulation time
$ns at 5.10 "finish"

#Print CBR packet size and interval
puts "CBR packet size = [$cbr2 set packet_size_]"
puts "CBR interval = [$cbr2 set interval_]"

# Run the simulation
$ns run

# close $tf


