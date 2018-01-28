#!/usr/bin/perl
use warnings;
use strict;
use Cwd;
use File::Basename;

paramCheck();

my $dump1 = shift;
my $dump2 = shift;

my $output_path = dirname(Cwd::abs_path($0));
my $parent_path = dirname($dump1);

if($parent_path eq '.') {
	$parent_path = $output_path;
	$dump1 = $output_path."/".basename($dump1);    
	$dump2 = $output_path."/".basename($dump2);    
} else {
	$dump1 = $parent_path."/".basename($dump1);
	$dump2 = $parent_path."/".basename($dump2);
}


open FILE1,"<","$dump1" or die "[*** Cannot open file! ***]";
open FILE2,"<","$dump2" or die "[*** Cannot open file! ***]";

my %file2;

# Read file2 in to hash
while(<FILE2>) {
	chomp;
	my($k,$v) = split /\<\=\>/;
	$file2{$k} = $v;
}


# Main loop
while(<FILE1>) {
	chomp;
	my($tmpK,$tmpV) = split /\<\=\>/;	

	my $bingo = 0;
	my $key;
	my $value;

	while(($key,$value) = each %file2) {

		if ($tmpK eq $key) {
			$bingo = 1;	
		  	unless ($tmpV eq $value) {
				printf("%-60s",$tmpK);
				printf("%3s","|X|");
				printf("%60s",$key);
				print "\n";
			}
			delete $file2{$key};
		}
	}

	if($bingo == 0) {
		printf("%-60s",$tmpK);
		printf("%3s","|?|");
		printf("%60s","?");
		print "\n";
	}
}


foreach(keys %file2) {
	printf("%-60s","?");
	printf("%3s","|?|");
	printf("%60s",$_);
	print "\n";

}

	

#select STDOUT;
close FILE1;
close FILE2;

### All Subs Goes Here ###
sub paramCheck {
        unless ($#ARGV == 1 && -f $ARGV[0] && -f $ARGV[1]) {
                print "Error !\n";
                print "Usage: $0 Absolute/pathname/to/dump/file\n";
                exit -1;
        }
}
