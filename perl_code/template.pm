package Template;

use warnings;
use strict;

require Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw(hello);

sub hello {
	my $name = shift;
	print "hello, $name\n";
}

1;
