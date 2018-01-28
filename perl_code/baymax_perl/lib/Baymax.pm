package Baymax;
use Mojo::Base 'Mojolicious';

use DBI;
use Cwd;

###### THIS METHOD WILL RUN ONCE AT SERVER START ######
sub startup {
	my $self = shift;

	my $DB_PATH = getcwd."/db/baymax.db";
	my $dbh = DBI->connect("dbi:SQLite:$DB_PATH") or die "Can not connect to SQLite:$!";
	$self->helper(db => sub { $dbh });

	$self->session(logged_in=>0);
	$self->secrets(['rockyourbodybitches','iwillreturn']);
	$self->sessions->cookie_name('helloiambaymax');
	$self->sessions->default_expiration('600');
	
	# Router
	my $r = $self->routes;
	
	# Normal route to controller
	$r->get('/')->to('login#login');
	$r->post('/')->to('login#auth');
	#$r->get('/login')->to('login#login');
	#$r->post('/login')->to('login#auth');

	my $auth = $r->under->to('login#isLogged');

	#######################
	###### Kit route ######
	#######################
	###### Page ######
	$auth->get('/kit')->to('kit#home');
	$auth->get('/host_probe_html')->to('kit#hostProbeHTML');
	$auth->get('/remote_command_html')->to('kit#remoteCommandHTML');
	$auth->get('/host_mng_html')->to('kit#hostMngHTML');
	$auth->get('/host_list_html')->to('kit#hostListHTML');
	$auth->get('/host_modify_html')->to('kit#hostModifyHTML');

	###### Function ######
	
	### Home Page ###

	### Host Probe Page ###
	$auth->post('/probe_host_info')->to('Kit::HostProbe#probeHostInfo');

	### Host Management Page ###
	$auth->post('/add_host')->to('Kit::HostMng#addHost');
	$auth->post('/delete_host')->to('Kit::HostMng#deleteHost');
	$auth->post('/verify_host')->to('Kit::HostMng#verifyHost');
	
	$r->get('/logout')->to('login#logout');
	
	# Route for development
	#$r->get('/dev/:usr')->to('dev#hello');	
	$r->get('/dev/:usr')->to('dev#hello',secret=>'$');	
	$r->get('/count')->to('dev#count');
}

1
