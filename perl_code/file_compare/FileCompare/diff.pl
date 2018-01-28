#!/usr/bin/perl -w
use strict;



paramCheck();

my $dump1 = $ARGV[0];
my $dump2 = $ARGV[1];


open FILE1,"<","$dump1" or die "Cannot open file!";
open FILE2,"<","$dump2" or die "Cannot open file!";
#open OUT,">>","/root/dircomp/out" or die "Cannot open file!";

my %file2;

# Read file2 in to hash
while(<FILE2>) {
	chomp;
	my($k,$v) = split /\<-\>/;
	$file2{$k} = $v;
}


# Main loop
while(<FILE1>) {
	chomp;
	my($tmpK,$tmpV) = split /\<-\>/;	

	my $bingo = 0;
	my $key;
	my $value;

	while(($key,$value) = each %file2) {

		if ($tmpK eq $key) {
			$bingo = 1;	
		  	unless ($tmpV eq $value) {
				printf("%-80s",$tmpK);
				printf("%3s","|X|");
				printf("%80s",$key);
				print "\n";
			}
			delete $file2{$key};
		}
	}

	if($bingo == 0) {
		printf("%-80s",$tmpK);
		printf("%3s","|?|");
		printf("%80s","?");
		print "\n";
	}
}


foreach(keys %file2) {
	printf("%-80s","?");
	printf("%3s","|?|");
	printf("%80s",$_);
	print "\n";

}

	

#select STDOUT;
close FILE1;
close FILE2;


sub paramCheck {
        unless ($#ARGV == 1 && $ARGV[0] =~ /^\// && -f $ARGV[0] && $ARGV[1] =~ /^\// && -f $ARGV[1]) {
                print "Error !\n";
                print "Usage: $0 Absolute/pathname/to/dump/file\n";
                exit -1;
        }
}
