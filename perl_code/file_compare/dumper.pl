#!/usr/bin/perl
use warnings;
use strict;
use Cwd;
use Digest::MD5;
use File::Basename;

paramCheck();

my $param = shift;
my $output_path = dirname(Cwd::abs_path($0));
my $parent_path = dirname($param);
my $target;

if($parent_path eq '.') {
	$parent_path = $output_path;
	$target = $output_path."/".basename($param);    
} else {
	$target = $parent_path."/".basename($param);
}

dumper($target);

### All Subs Goes Here ###

sub paramCheck {
	unless ($#ARGV == 0 && -d $ARGV[0]) {
		print "Error !\n";
		print "Usage: $0 Path_to_target_directory \n";
		exit -1;
	}
}
	

sub getFileMD5 {
	unless ( $#_ == 0 && -f $_[0] ) {
		if (-d $_[0]) {
			return "d";
		} else {
			print "[*** (getFileMD5) parameter error ! ***]\n";
		}
	}	

	open ( my $fh,'<',$_[0]) or die "Cannot open file in [getFileMD5] !";
	binmode($fh);
	return Digest::MD5->new->addfile($fh)->hexdigest;	
	close($fh);
}


sub dumper {
        my $path = shift;
        my @dirs = ($path);

	open (OUT,">>","$output_path/dump.".int(rand(1000)+1) ) or die "[*** Cannot open file in sub (dumper) ***]";
	select OUT;

        my $dir;
        my $file;

        while($dir = pop(@dirs)) {
				local *FH;
				opendir (FH,$dir) or die "Cannot open $dir in sub [dumper]";

                foreach (readdir(FH)) {
					next if ($_ eq "." || $_ eq "..");
					$file = $dir."/".$_;
					
					if ((! -l $file) && -d $file) {
						push(@dirs,$file);
					}

					my $md5 = getFileMD5($file);
					$file =~ s#$parent_path\/##;
					print OUT "$file\<\=\>$md5\n";
				}
				close FH;
        }
	select STDOUT;
	close OUT;
}
