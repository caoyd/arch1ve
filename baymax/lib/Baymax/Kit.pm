package Baymax::Kit;
use Mojo::Base 'Mojolicious::Controller';


###### PAGE RENDER ######
sub home {
	my $self = shift;
	$self->render(template=>'kit/home',username=>$self->session->{'logged_user'});
}
sub hostProbeHTML {
	my $self = shift;
	$self->render(template=>'kit/host_probe');
}
sub remoteCommandHTML {
	my $self = shift;
	$self->render(template=>'kit/remote_command');
}

sub hostMngHTML {
	my $self = shift;
	$self->render(template=>'kit/host_mng');
}

sub hostListHTML {
	my $self = shift;
	my $filter =  $self->param("filter_param");

	if(defined($filter)) {
		$self->render(template=>'kit/host_list',stat=>$filter);
	} else {
		$self->render(template=>'kit/host_list',stat=>"all");
	}
}
sub hostModifyHTML {
	my $self = shift;
	$self->render(template=>'kit/host_modify');
}



1;
