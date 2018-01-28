#!/usr/bin/env perl
###### AUTHOR           Skipper
###### DESCRIPTION      Return network traffics (RX/TX) of all network
######                  interface (Use it with "watch" together)
###### VERSION          v1.3
###### UPDATE           2015/08/13
use strict;
use warnings;


my $a =  sample();
sleep 1;
my $b = sample();

print "+------------------+------------------+------------------+\n";
print "|";
printf("%19s","Network Interface |");
printf("%19s","RX |");
printf("%19s","TX |");
print "\n";
print "+------------------+------------------+------------------+\n";

foreach(keys %$a) {
	print "|";
	printf("%19s","$_ |");
	printf("%19s",formatBandwidth($b->{$_}->[0]-$a->{$_}->[0])." |");
	printf("%19s",formatBandwidth($b->{$_}->[1]-$a->{$_}->[1])." |");
	print "\n";
	print "+------------------+------------------+------------------+\n";
}



##############################
###### ALL SUBS GO HERE ######
##############################
sub sample {
	open(NET,"< /proc/net/dev") or die "Error in sub [sample]:$!";

	### %sample = (
	### 	"eth0" => [bytes_RX,bytes_TX],
	### 	"eth1" => [bytes_RX,bytes_TX],
	### 	......
	### )
	my %sample;
	my @tmp;

	while(<NET>) {
		chomp();
		if(/:/) {
			s/^\s+//g;
			my($k,$v) = split /:/,$_;
			$v =~ s/^\s+//g;
			@tmp = split /\s+/,$v;
			$sample{$k} = [ $tmp[0],$tmp[8] ];
		}
	}
	close NET;
	return \%sample;
}


sub formatBandwidth {
	my $speed = shift;
	my $unit;

	### < 1024 - bps
	### 1024 - Kbps
	### 1048576(1024*1024) - Mbps
	### 1073741824(1024*1024*1024) - Gbps
	
	if($speed >= 1073741824) {
		$speed /= 1073741824;
		$speed = sprintf("%.2f",$speed);
		$unit = "Gbps";
		return "$speed$unit";
	} elsif($speed >= 1048576) {
		$speed /= 1048576;
		$speed = sprintf("%.2f",$speed);
		$unit = "Mbps";
		return "$speed$unit";
		
	} elsif($speed >= 1024) {
		$speed /=1024;
		$speed = sprintf("%.2f",$speed);
		$unit = "Kbps";
		return "$speed$unit";
		
	} else {
		$unit = "bps";
		return "$speed$unit";
	}
}### formatBandwidth
