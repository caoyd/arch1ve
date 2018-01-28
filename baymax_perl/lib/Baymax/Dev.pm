package Baymax::Dev;
use Mojo::Base 'Mojolicious::Controller';


# This action will render a template
sub hello {
	my $self = shift;
 	my $people = $self->param('usr');
	my $shoo = $self->param('secret');

	$self->render(text=>"Good to see you, $people with a $shoo");
	
}

sub count {
	my $self = shift;
	$self->session->{counter}++;

	$self->render();
}

1;
