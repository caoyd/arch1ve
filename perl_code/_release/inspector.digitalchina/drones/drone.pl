#!/usr/bin/env perl
###### AUTHOR           Skipper.D
###### DESCRIPTION      Output only inspect-specific information of
######                  CPU, memory, disk and process.
###### VERSION          v1.3
###### UPDATE           2015/08/25
use warnings;
use strict;

################## CPU INFO ##################
open(CPU,"<","/proc/loadavg") or die "OPEN '/proc/loadavg' ERROR :/";
my $currentLoad = readline(CPU);
chomp($currentLoad);
$currentLoad =~ s/\s[0-9]\/.*//;
close CPU;
print "[ CPU ]\n";
print "-------------------+-------------------+\n";
printf("%20s","Current Load |");
printf("%20s","$currentLoad |");
print "\n";
print "-------------------+-------------------+\n";

################## Memory INFO ##################
open(MEM,"<","/proc/meminfo") or die "OPEN '/proc/meminfo' ERROR :/";
my @mem_tmp;
my $mem_total;
my $mem_free;
my $swap_total;
my $swap_free;
while(<MEM>) {
    if(/MemTotal/) {
        @mem_tmp = split(/\s+/,$_);
        $mem_total = $mem_tmp[1];
    }
    if(/MemFree/) {
        @mem_tmp = split(/\s+/,$_);
        $mem_free = $mem_tmp[1];
    }
    if(/SwapTotal/) {
        @mem_tmp = split(/\s+/,$_);
        $swap_total = $mem_tmp[1];
    }
    if(/SwapFree/) {
        @mem_tmp = split(/\s+/,$_);
        $swap_free= $mem_tmp[1];
    }
}
my $mem_used = $mem_total - $mem_free;
my $swap_used = $swap_total - $swap_free;
$mem_used = sprintf("%d",$mem_used/1024);
$mem_free= sprintf("%d",$mem_free/1024);
$swap_used = sprintf("%d",$swap_used/1024);
$swap_free= sprintf("%d",$swap_free/1024);
close MEM;
print "[ Memory ]\n";
print "-------------------+-------------------+\n";
printf "%20s","Memory(MB) |";
printf "%20s","Swap(MB) |";
print "\n";
print "-------------------+-------------------+\n";
printf "%10s","USED";
printf "%10s","FREE |";

printf "%10s","USED";
printf "%10s","FREE |";
print "\n";
print "-------------------+-------------------+\n";
printf "%10s",$mem_used;
printf "%10s",$mem_free." |";
printf "%10s",$swap_used;
printf "%10s",$swap_free." |";
print "\n";
print "-------------------+-------------------+\n";


################## Disk INFO ##################
my @disk_tmp = `/bin/df -Th`;
my %partition;
foreach(@disk_tmp) {
    if(/ext2|ext3|ext4|xfs/) {
        my @tmp = split(/\s+/,$_); 
        @tmp = reverse(@tmp);
        $partition{$tmp[0]} = [ $tmp[1],$tmp[2],$tmp[3] ] ;
    }
}

my @sorted_key = sort(keys %partition);
my $num = $#sorted_key +1;
print "[ Disk ]\n";
diskBorder($num);
foreach(@sorted_key) {
    printf "%20s","$_ |";
}
print "\n";
diskBorder($num);
diskTitle($num);
diskBorder($num);
foreach(@sorted_key) {
    printf "%10s","$partition{$_}->[0]($partition{$_}->[2])";
    printf "%10s","$partition{$_}->[1] |";
}
print "\n";
diskBorder($num);


################## Process INFO ##################
if($#ARGV > -1) {
	my @keyword = split /,/,shift;
	print "[ Process ]\n";
	print "-------------------+---------+---------+\n";
	printf("%20s",'Name |');
	printf("%10s",'PID |');
	printf("%10s",'Port |');
	print "\n";
	print "-------------------+---------+---------+\n";
	foreach(@keyword) {
		my $ref = getPIDAndPort($_);
		printf("%20s","$_ |");
		printf("%10s","${$ref}[0] |");
		printf("%10s","${$ref}[1] |");
		print "\n";
		print "-------------------+---------+---------+\n";
	}
}


##############################
###### ALL SUBS GO HERE ######
##############################
sub diskBorder {
    my $num = $_[0];
    for(my $i=0;$i<$num;$i++) {
        print "-------------------+";
    }
    print "\n";
}
sub diskTitle {
    my $num = $_[0];
    for(my $i=0;$i<$num;$i++) {
        printf "%10s","USED";
        printf "%10s","AVAIL |";
    }
    print "\n";
}

sub printDiskInfo {
	my $count;
	my $i;

	my @tmp = keys %{$_[0]};
	$count = $#tmp + 1;

	while(my($k,$v) = each %{$_[0]}) {
		printf "%10s","$$v[3]($$v[2])";
		printf "%10s","$$v[4] |";
	}
	print "\n";
	for($i=0;$i<$count;$i++) {
		print "-------------------+";
	}
}
sub getPIDAndPort {
	my $kw = shift; 
	my $pid = getPID($kw);
	if($pid ne "null"){
		my $tmp = `sudo netstat -tlnp | grep $pid`;
		if($tmp =~ /:([0-9]{1,5})\s/) {
			return [$pid,$1];
		} else {### pid exists but no port
			return [$pid,"null"];
		}
	} else {
		return ["null","null"];
	}
} 

sub getPID {
	my $keyword = shift; 
	my $pid_hash;
	my $PROC_DIR  = "/proc";
	chdir $PROC_DIR;
	my @pids = glob "[0-9]*";
	
	### assemble pid and cmdline into hash ($pid_hash)
	foreach(@pids) {
		open(FH,"$_/cmdline") or die "open $_ cmdline error $!";
		while(my $line = <FH>) {
			$pid_hash->{$_} = $line;
		}
		close FH;
	}

	delete $pid_hash->{"$$"}; 
	foreach (keys %$pid_hash ) {
		return $_ if $pid_hash->{$_} =~ /$keyword/;
	}
	return "null";# "no process pid"
}
