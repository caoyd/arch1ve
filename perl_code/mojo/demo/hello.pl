#!/usr/bin/perl
use warnings;
use strict;

use Mojolicious::Lite;

get '/' => sub {
	my $c = shift;

	$c->render(text => "hello Skipper!");
};

app->start('daemon');
