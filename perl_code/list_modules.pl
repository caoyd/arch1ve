#!/usr/bin/env perl
use warnings;
use strict;

use ExtUtils::Installed;
my $mods = ExtUtils::Installed->new();

foreach($mods->modules()) {
	print $_."---";
	print $mods->version($_),"\n";
}
