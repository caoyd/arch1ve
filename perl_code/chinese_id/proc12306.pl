#!/usr/bin/perl -w
use strict;
use LWP;

$|=1;
my @infotmp;

open FH,'<12306.proc.txt' or die "open file error";

while(<FH>) {
	chomp;
	@infotmp = split /\s/,$_;
	print $infotmp[1]."---".$infotmp[0]."---".&getaddr($infotmp[0])."\n";
}

sub getaddr {
	my @htmltmp;
	my $req= LWP::UserAgent->new();
	my $resp = $req->post("http://www.cz88.net/tools/id.php",["in_id"=>$_[0]]) or die "error";
	my @result = split /\n/,$resp->content;

	foreach(@result) {
	    if( $_ =~ m#div class="data">(.*)?</div>#) {
		        push @htmltmp,$1;
		}
	}
	return $htmltmp[0];
	$#htmltmp = -1;
}
