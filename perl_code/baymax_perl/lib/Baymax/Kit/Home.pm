package Baymax::Kit::HostProbe;
use Mojo::Base 'Mojolicious::Controller';
use Cwd;
use Net::SSH2;
use JSON;

my $APP_PATH		= getcwd;
my $DRONE		= $APP_PATH."/drone/drone";
my $DST_FILE= "/tmp/drone";


sub probeHost {
	my $self = shift;
	my $ip		= $self->param("ip_param");
	my $port	= $self->param("port_param");
	my $login_usr	= $self->param("login_usr_param");
	my $login_psd	= $self->param("login_psd_param");
	
	my $resp = launchDrone($ip,$port,$login_usr,$login_psd);
	my $json = encode_json $resp;
	$self->render(text=>$json);
}

sub launchDrone {
	my($ip,$port,$usr,$psd) = @_;
	my %result;
	
	### Transport drone file ###
	my $warpgate = Net::SSH2->new;
	$warpgate->connect($ip,$port) or die "Error connecting host:$!";	
	if($warpgate->auth_password($usr,$psd)) {
		$warpgate->scp_put($DRONE,$DST_FILE);

		my $selfChannel = $warpgate->channel();
		$selfChannel->shell();
		print $selfChannel "perl $DST_FILE\n";
		while(<$selfChannel>) {
			%result =  split /---/,$_;
		}
	}
	return \%result;
}
1;
