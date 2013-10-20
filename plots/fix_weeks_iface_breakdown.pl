#!/usr/bin/perl
# This file fixes the week numbers for the pl-mapping dataset for
# the files produced by generateInterfaceBreakdown.py

sub remap_week {
    my $week = shift;
    return $week if ($week <= 20);
    return $week+7 if ($week <= 22);
    return $week+8;
}

sub printzeros {
    my ($week, $n) = @_;
    print "$week\t" . join("\t", map {"0"} (1..$n)) . "\n";
}

my $nf;

while(<>) {
	chomp;
	#count fields
	@fields = split /\t/;
	if ($fields[0] =~ /^# Week/) {
		$nf = scalar(@fields) - 1;
		print STDERR "File has $nf fields\n";
		print "$_\n";
	} elsif ($fields[0] =~ /^#/) {
		next;
	} else {
		if (!defined $nf) {
			die "Couldn't read number of fields before data.\n";
		}
		$week = $fields[0];
		if ($week == 9 || $week == 10) {
			print "#". $_ . "\n";
			&printzeros($week, $nf);
		} elsif ($week == 20) {
			print "$_\n";
			for $i (21..27) {
				&printzeros($i, $nf);
			}
		} elsif ($week == 22) {
			$fields[0] = &remap_week($fields[0]);
			print join("\t",@fields) . "\n";
			&printzeros(30, $nf);
		} else {
			$fields[0] = &remap_week($fields[0]);
			print join("\t",@fields) . "\n";
		}
	}
}

