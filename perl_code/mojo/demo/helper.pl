#!/usr/bin/perl -w
use strict;

use Mojolicious::Lite;

helper whois => sub {
	my $c		= shift;
	my $agent	= $c->req->headers->user_agent || "Anonymous";
	my $ip		= $c->tx->remote_address;
	return "$agent ($ip)";
};


get '/secret';

app->start('daemon');

__DATA__
@@ secret.html.ep
We know who you are <%= whois %>
