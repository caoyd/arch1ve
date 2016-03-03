#!/usr/bin/perl -w
use strict;

use Mojolicious::Lite;

get '/foo' => sub {
	my $c = shift;
	$c->stash(one => 23);
	$c->render(template => 'magic',two => 24);
};

app->start('daemon');

__DATA__

@@ magic.html.ep
The magic numbers are <%= $one %> and <%= $two %>.
