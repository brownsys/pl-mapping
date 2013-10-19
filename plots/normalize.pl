#!/usr/bin/perl

#use strict;

my $usage = "$0 <router degree dist file>\n";

my %count;
my ($degree, $week);
die $usage unless scalar(@ARGV) == 1;

#read once for count of entries per week
open FIN, $ARGV[0] or die "Can't open $ARGV[0]\n";
while(<FIN>) {
    chomp;
    ($degree, $week) = split;
    $count{$week}++;
}
close FIN;

open FIN, $ARGV[0] or die "Can't open $ARGV[0]\n";
open FOUT, ">$ARGV[0].norm" or die "Can't create $ARGV[0].norm";

$count = 0;
while(<FIN>) {
    chomp;
    @F = split;
    if (/#/) {
        print FOUT "$_\n";
    } elsif (scalar @F == 0) {
        print FOUT "$_\n";
        $count = 0;
    } else {
        ($degree, $week) = ($F[0], $F[1]);
        $N = $count{$week};
        $count++;
        if ($week != 10) {
            print FOUT "$degree $week $count ".$count/$N." \n";
        } 

    }
}    
close FOUT;
close FIN;
