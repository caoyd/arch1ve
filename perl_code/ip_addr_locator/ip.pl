#!/usr/bin/perl -w
use strict;

use LWP::Simple;

open (IPFILE,"<ip_20151010.txt") or die "Open file error!";
while(<IPFILE>) {
	chomp();
	my @tmp = split /:/,$_;
	my $ipaddr = $tmp[0];	
	my $url = "http://ip138.com/ips1388.asp?ip=".$ipaddr."&action=2";
	my $content = get($url);
	die "Get URL error!" unless defined $content;
	
	my @content = split /\n/,$content;
	
	foreach (@content) {
		if( $_ =~ m#ul class="ul1"><li>(.*?)</li><li>#) {
			print $tmp[1]."--".$tmp[0]."--".$1."\n";
		}
	}
}
