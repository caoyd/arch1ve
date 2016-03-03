#!/usr/bin/env perl
####### AUTHOR           Skipper
####### DESCRIPTION      batch replacement
####### VERSION          v1.1
####### UPDATE           2015/07/02

use warnings;
use strict;
use File::Find;

use vars qw/*name *dir *prune/;
*name   = *File::Find::name;
*dir    = *File::Find::dir;
*prune  = *File::Find::prune;

my $BACKUP='yes';# yes:backup,no:do not backup
my $SEARCH_DIR='/root/temp';
my $KEYWORD="apple";
my $REPLACEMENT_FILE="apple.txt";

my @files;

unless(-d $SEARCH_DIR) {
	print "Can not find $SEARCH_DIR\n";
	exit -1;
}
unless(-e $REPLACEMENT_FILE) {
	print "Can not find $REPLACEMENT_FILE\n";
	exit -1;
}

File::Find::find({wanted => \&wanted}, $SEARCH_DIR);
my $timestamp = getTime();
my $num = $#files + 1;

if($BACKUP eq 'yes') {
	foreach(@files) {
		rename $_,$_.".$timestamp";
		system '/bin/cp','-f',$REPLACEMENT_FILE,$_;	
	}
	
	print "Backup $num files\n";
	print "Replace $num files\n";
} else  {
	foreach(@files) {
		system '/bin/cp','-f',$REPLACEMENT_FILE,$_;
	}
	print "Replace $num files\n";
}


##############################
###### ALL SUBS GO HERE ######
##############################
sub wanted {
    /^.*$KEYWORD.*\z/s
    && push @files,$name;
}

sub getTime {
	my @time = localtime(time);
	my $year = $time[5] + 1900;
	my $month = $time[4] + 1;
	my $formated_time = $year."_".$month."_".$time[3].'.'.$time[2]."_".$time[1]."_".$time[0];
	return $formated_time;
}
