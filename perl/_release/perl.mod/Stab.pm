package Stab;
####### AUTHOR           Skipper.D
####### DESCRIPTION      Format output data into table
####### VERSION          v1.0
####### UPDATE           2015/08/25
use warnings;
use strict;

require Exporter;
our @ISA = qw(Exporter);
our @EXPORT_OK = qw(tableHeader tableBody);


###### Parameter
###### 1st - array ref like ["a","b","c"]
###### 2nd - cell width
###### 3rd - margin
###### 4th - top: 0-no top, 1-with top
sub tableHeader {
	my $arr_ref 	= shift;
	my $cell_num 	= $#{$arr_ref}+1;
	my $cell_width 	= shift;
	my $margin 		= shift;
	my $top 		= shift;

	if($top == 1) {
		buildBorderLine($cell_num,$cell_width,$margin);
		buildContentLine($arr_ref,$cell_width,$margin);
		buildBorderLine($cell_num,$cell_width,$margin);
	} else {
		buildContentLine($arr_ref,$cell_width,$margin);
		buildBorderLine($cell_num,$cell_width,$margin);
	}
		
}

###### Parameter 
###### 1st - array ref like [["a","b","c"],
######                        ["a","b","c"],
######                        ["a","b","c"]]
###### 2nd - cell width
###### 3rd - margin
sub tableBody {
	my $arr_ref 	= shift;
	my $cell_num 	= $#{$arr_ref->[0]}+1;
	my $cell_width 	= shift;
	my $margin 		= shift;

	foreach(@$arr_ref) {
		buildContentLine($_,$cell_width,$margin);
		buildBorderLine($cell_num,$cell_width,$margin);
	}
}




###### Parameter
###### 1st - cell number
###### 2nd - cell width
###### 3rd - margin
sub buildBorderLine {
	my $num = shift;
	my $width = shift;
	my $margin = shift;

	buildLeftMargin($margin,'+');	
	for(my $i=0;$i<$num;$i++) {
		print "-"x$width,"+";
	}
	print "\n";
}

###### Parameter
###### 1st - cell number
###### 2nd - cell width
###### 3rd - margin
sub buildContentLine {
	my $arr_ref = shift;
	my $width = shift;
	my $margin = shift;

	buildLeftMargin($margin,'|');	
	foreach(@$arr_ref) {
		 my $space_num = $width-length($_)-1;
		 print " "x$space_num,$_," |";
	}
	print "\n";
}



###### Parameter
###### 1st - margin
###### 2nd - symbol: '+','|'
sub buildLeftMargin {
	my $margin = shift;
	my $symbol = shift;

	if($margin == 0) {
		print "$symbol";
	} else {
		print " "x$margin,"$symbol";
	}
}


1;
