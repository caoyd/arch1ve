#!/usr/bin/perl -w
use strict;

use Mojolicious::Lite;

get '/' => sub {
	my $c = shift;
	$c->render;
} => 'index';

get '/hello';

app->start('daemon');

__DATA__

@@ index.html.ep
<%= link_to Hello => 'hello' %>.
<%= link_to Reload => 'index' %>.

@@ hello.html.ep
Hello Skipper!
