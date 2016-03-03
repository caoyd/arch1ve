#!/usr/bin/perl
###### AUTHOR           Skipper.D
###### DESCRIPTION      Connect to host and send out the "drone"
######                  to get target host's information
######                  (cpu,memory,disk,process)
###### VERSION          v1.8
###### UPDATE           2015/09/15
use warnings;
use strict;
use File::Spec;
use Net::OpenSSH;
use POSIX qw/strftime/;

print "Inspect Initializing...\n\n";

my $time = strftime "%y-%m-%d %H:%M",localtime;
my $absPath = File::Spec->rel2abs(__FILE__);
my($vol,$cwd,$file) = File::Spec->splitpath($absPath);
my $CONF= $cwd."CONF_cq";
my $DRONE = $cwd."drones/drone";


open(TGT,"<",$CONF) or die "OPEN CONF ERROR :/";
while(<TGT>) {
	chomp();
    next if /^#/;
    next if /^$/;
    
	my @param = split /\|/,$_;
	push(@param,$DRONE);
	launchDrone(\@param);
}

#print "+---------------------------------------------+\n";
#print "| 项目名称 | 成都市市民融合服务平台           |\n";
#print "+---------------------------------------------+\n";
#print "| 巡检单位 | 智慧神州（成都）运营服务有限公司 |\n";
#print "+---------------------------------------------+\n";
#print "| 巡检时间 |";
#printf(" %-33s",$time);
#print "|\n";
#print "+---------------------------------------------+\n";
#print "| 责任人   | 技术部-张鹏                      |\n";
#print "+---------------------------------------------+\n";


##############################
###### ALL SUBS GO HERE ######
##############################
sub launchDrone {
	my $param_ref = shift;
	my $len = $#{$param_ref};
	my($ip,$port,$usr,$psd,$domain,$param,$file);

	if($len == 6){
		($ip,$port,$usr,$psd,$domain,$param,$file) = @{$param_ref};
	} else {
	#array len 5
		($ip,$port,$usr,$psd,$domain,$file) = @{$param_ref};
	}

	my $DST_FILE = "/tmp/drone";
	my $result;

	my $warpgate = Net::OpenSSH->new($ip, port => $port, user => $usr, password => $psd,
									timeout=>20,master_opts => [-o => "StrictHostKeyChecking=no"]);
	$warpgate->error and die "Connect error".$warpgate->error;
	$warpgate->scp_put($file,$DST_FILE) or die "SCP error".$warpgate->error;
	print "-------------------+-------------------+\n";
	printf("%20s","$ip |");
	printf("%20s","$domain |");
	print "\n";
	print "-------------------+-------------------+\n";
	
	if($len == 6) {
		print $warpgate->capture("python $DST_FILE $param");
	} else {
		print $warpgate->capture("python $DST_FILE");	
	}
	
	print "\n\n\n\n";
}
