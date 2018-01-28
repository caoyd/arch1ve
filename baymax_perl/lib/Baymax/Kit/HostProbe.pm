package Baymax::Kit::HostProbe;
use Mojo::Base 'Mojolicious::Controller';
use Cwd;
use Net::OpenSSH;
use JSON;

my $APP_PATH		= getcwd;
my $DRONE		= $APP_PATH."/drone/drone";
my $DST_FILE= "/tmp/drone";


sub probeHostInfo {
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
	my $warpgate = Net::OpenSSH->new($ip,port=>$port,user=>$usr,password=>$psd,
									timeout=>10,master_opts => [-o => "StrictHostKeyChecking=no"]);
	$warpgate->error and die "Connection fail".$warpgate->error; 
	$warpgate->scp_put($DRONE,$DST_FILE);

	my $tmp = $warpgate->capture("perl $DST_FILE");
	%result = split /---/,$tmp;
	
	return \%result;
}

1;
