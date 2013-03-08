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

# Create nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

#Create links between the nodes
$ns duplex-link $n1 $n2 10Mb 10ms DropTail
$ns duplex-link $n2 $n5 10Mb 10ms DropTail
$ns duplex-link $n2 $n3 10Mb 10ms DropTail
$ns duplex-link $n3 $n4 10Mb 10ms DropTail
$ns duplex-link $n3 $n6 10Mb 10ms DropTail


# Connect Node 1 and Node 4 with a TCP stream

set tcp1 [new Agent/TCP]
$ns attach-agent $n1 $tcp1
$tcp1 set fid_ 1

set sink4 [new Agent/TCPSink]
$ns attach-agent $n4 $sink4
$sink4 set fid_ 4

$ns connect $tcp1 $sink4


# Connect N2 and N3

set udp2 [new Agent/UDP]
$ns attach-agent $n2 $udp2
$udp2 set fid_ 2

set null3 [new Agent/Null]
$ns attach-agent $n3 $null3
$null3 set fid_ 3

$ns connect $udp2 $null3


# Set up CBR and attach to $udp2

set cbr2 [new Application/Traffic/CBR]
$cbr2 set interval_ 0.005
$cbr2 set type_ CBR
$cbr2 set packet_size_ 1000
$cbr2 set rate_ 1mb
$cbr2 set random_ false

$cbr2 attach-agent $udp2


# set tcp [new Agent/TCP/{Reno, Newreno, Vegas}]  #for others

# Schedule events for the CBR and FTP agents
$ns at 0.05 "$cbr2 start"
$ns at 0.01 "$tcp1 start"
$ns at 4.50 "$tcp1 stop"
$ns at 5.00 "$cbr2 stop"

#Detach tcp and sink agents (not really necessary)
# $ns at 4.5 "$ns detach-agent $n0 $tcp ; $ns detach-agent $n3 $sink"

#Call the finish procedure after 5 seconds of simulation time
$ns at 5.0 "finish"

#Print CBR packet size and interval
puts "CBR packet size = [$cbr2 set packet_size_]"
puts "CBR interval = [$cbr2 set interval_]"

#Run the simulation
$ns run



close $tf

