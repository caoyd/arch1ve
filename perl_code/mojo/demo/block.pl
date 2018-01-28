#!/usr/bin/perl -w 
use strict;

use Mojolicious::Lite;

get '/with_block' => 'block';

app->start('daemon');

__DATA__

@@ block.html.ep
% my $link = begin
	% my($url,$name) = @_;
		try <%= link_to $url => begin %>
		<%= $name %>.
		<% end %>

% end
<!DOCTYPE html>
<html>
	<head><title>hahahaha</title></head>
	<body>
		%= $link->('http://mojolicio.us','Mojolicious')
		%= $link->('http://www.mop.com','Mop')
	</body>
</html>
