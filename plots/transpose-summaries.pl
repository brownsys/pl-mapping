#!/usr/bin/perl
# Script to get each of the SUMMARY.txt from the pl_archives directory and prints the content
# of each one in one line, successively
# Used to generated summary-transpose.txt, used to plot the statistics of DNS collection over
# all weeks.
#
# EXPECTS: a directory with a numeric subdirectories containing a SUMMARY.txt file each, with
#         the keys listed in @keys, in the same order.

use strict;

sub remap_week {
	my $week = shift;
    	return ($week <= 20)?$week:$week+7;
}

my $usage = "$0 <pl_archives directory>\n";
die $usage unless scalar(@ARGV) > 0;

my $dir = $ARGV[0];

opendir my($dh), $dir or die "Can't open $dir\n";
my @weeks = readdir $dh;
closedir $dh;

my $weekdir;
my @keys = ('exist', 'atlas', 'demarc', 'dial', 'cogent-other', 'non-cogent',
            'NXDOMAIN', 'SERVFAIL', 'REFUSED', 'timeout', 'alias', 'no-PTR', 'anomaly-lines');
my ($key, $value);
my $i;
my $expected;

#header
print "# week " . (join " ",@keys) . "\n";
#data lines
for $weekdir (grep {/\d+/} sort {$a <=> $b} (@weeks)) {
    open FIN, "$dir/$weekdir/SUMMARY.txt" or die "Can't open $dir/$weekdir/SUMMARY.txt\n";
    $i = 0;
    print &remap_week($weekdir)." ";
    while(<FIN>) {
	chomp;
        ($key,$value) = $_ =~ /Num\s+([^:]+):\s+(\d+)/;
        $key =~ s/ /-/g;
        if (defined $key) {
            die "Inconsistent key name $key (expected $keys[$i]) at $dir/$weekdir/SUMMARY.txt\n"
                if $key ne $keys[$i];
            print "$value ";
            $i++;
        }
       
    }
        if ($i) {
                print "\n";
        }
    close FIN;    
}


