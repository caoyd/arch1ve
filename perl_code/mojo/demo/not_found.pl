#!/usr/bin/perl -w
use strict;

use Mojolicious::Lite;

get '/missing' => sub { shift->render(template => 'does_not_exist') };

get '/dies' => sub { die 'International Error'};

app->start('daemon');
