package Baymax::Kit::HostMng;
use Mojo::Base 'Mojolicious::Controller';
use Net::OpenSSH;
use Cwd;
use DBI;


#my $DB_PATH = getcwd."/db/baymax.db";
#my $dbh = DBI->connect("dbi:SQLite:$DB_PATH") or die "Can not connect to SQLite:$!";
sub addHost {
	my $self = shift;
	my $ip				= $self->param("ip_param");
	my $hostname		= $self->param("hostname_param");
	my $login_usr		= $self->param("login_usr_param");
	my $login_psd		= $self->param("login_psd_param");
	my $port			= $self->param("port_param");
	my $distr			= $self->param("distr_param");
	my $note			= $self->param("note_param");
	
	my $sql = 'insert into host(ip,hostname,login_usr,login_psd,ssh_port,dist,note,verify) values("'.$ip.'","'.$hostname.'","'.$login_usr.'","'.$login_psd.'",'.$port.',"'.$distr.'","'.$note.'","no")';

	my $sth = $self->db->prepare($sql);
	$sth->execute;
	$self->render(template=>'kit/host_list',stat=>"all");
	$self->db->disconnect();	
}

sub verifyHost {
	my $self = shift;
	my $id = $self->param("host_id_param");
	my $sql = 'select ip,login_usr,login_psd,ssh_port from host where id='.$id;
	my $sth = $self->db->prepare($sql);
	$sth->execute;

	my($ip,$usr,$psd,$port);
	my $verify_result;
	my $flag = 1;
	
	while(my @result = $sth->fetchrow_array) {
		$ip		= $result[0];
		$usr 	= $result[1];
		$psd	= $result[2];
		$port	= $result[3];
	}


	my $warpgate = Net::OpenSSH->new($ip,port=>$port,user=>$usr,password=>$psd,
									timeout=>10,master_opts => [-o => "StrictHostKeyChecking=no"]);
	$warpgate->error and $flag = 0;
	if($flag == 0){
		$verify_result = "Connection Fail";
		$sql = 'update host set verify="no" where id='.$id;
		$sth = $self->db->do($sql);
	} else { 
		$verify_result = "Connection Success";
		$sql = 'update host set verify="yes" where id='.$id;
		$sth = $self->db->do($sql);
	}

	$self->render(template=>'kit/verify_result',result=>$verify_result);
	$self->db->disconnect();
}

sub updateHost {
}

sub deleteHost {
	my $self = shift;
	my $host_id = $self->param("host_id_param");
	my $sql = 'delete from host where id='.$host_id;
	my $sth = $self->db->prepare($sql);
	$sth->execute;
	$self->render(template=>'kit/host_list',stat=>"all");
}

1;
