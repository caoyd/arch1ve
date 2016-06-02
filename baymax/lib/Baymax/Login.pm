package Baymax::Login;
use Mojo::Base 'Mojolicious::Controller';

sub isLogged {
	my $self = shift;
	
	if($self->session->{'logged_in'}) {
		return $self;
	} else { 
		$self->redirect_to('/');
	}
}

sub userExists {
	my($username,$password) = @_;
	return 1 if($username eq 'skipper' && $password eq 'hello');
}


sub auth {
	my $self = shift;

	#if(!$self->session->{'logged_in'}) {
	
	my $loginID = $self->param('username');
	my $loginPSD= $self->param('password');

		if( userExists($loginID,$loginPSD) ) {

			# store session
			$self->session(logged_in=>1);
			$self->session(logged_user=>$loginID);

			# store value for next step
			$self->stash(username=>$loginID);
			$self->redirect_to('/kit');
		} else {
			$self->redirect_to('/');
		}
	#} else {
	#	$self->redirect_to('/kit',username=>$self->session->{'logged_user'});
	#}
}


sub login {
	my $self = shift;

	if($self->session->{'logged_in'}) {
		$self->redirect_to('/kit',username=>$self->session->{'logged_user'});
	} else {
		$self->render(template=>'index');  	
	}
}



sub logout {
	my $self = shift;
	$self->session(expires=>1);
	$self->redirect_to('/');
}
	

1;
