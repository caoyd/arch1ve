#!/usr/bin/perl -w
use strict;

# Create a user agent object
use LWP::UserAgent;
my $ua = LWP::UserAgent->new;
$ua->agent("MyApp/0.1 ");
 
# Create a request
my $req = HTTP::Request->new(POST => 'http://www.ip138.com/ips138.asp');
$req->content_type('application/x-www-form-urlencoded');
$req->content('ip="61.139.2.69"');
 
# Pass request to the user agent and get a response back
my $res = $ua->request($req);
 
# Check the outcome of the response
if ($res->is_success) {
    print $res->content;
}
else {
    print $res->status_line, "\n";
}
