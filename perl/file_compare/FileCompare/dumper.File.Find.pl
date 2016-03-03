#!/usr/bin/perl -w
use strict;


use Cwd;
use Digest::MD5;
use File::Find;
use File::Basename;

paramCheck();

my $dirpath = dirname($ARGV[0]);


my $outputPath = dirname(Cwd::abs_path($0));

find(\&processor,$ARGV[0]);


### Subroutine definition ###

sub paramCheck {
	unless ($#ARGV == 0 && $ARGV[0] =~ /^\// && -d $ARGV[0]) {
		print "Error !\n";
		print "Usage: $0 Absolute/pathname/of/directory \n";
		exit -1;
	}
}
	

sub getFileMD5 {
	unless ( $#_ == 0 && -f $_[0] ) {
		if (-d $_[0]) {
			return "d";
		} else {
			print "[getMD5] parameter error !\n";
		}
	}	

	open ( my $fh,'<',$_[0]) or die "Cannot open file in [getFileMD5] !";
	binmode($fh);
	return Digest::MD5->new->addfile($fh)->hexdigest;	
	close($fh);
}

sub processor {
	open (OUT,">>","$outputPath/dump") or die "Cannot open file in sub [processor]";
	select OUT;

	my $filename = $File::Find::name;
	my $md5 = getFileMD5($filename);
	$filename =~ s#$dirpath\/##;
	print OUT "$filename\<-\>$md5\n";

	select STDOUT;
	close OUT;
}
