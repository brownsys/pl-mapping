#!/usr/bin/perl

# Remap weeks in router_degree*.dat files
# Skip weeks 9 and 10

sub remap_week {
    my $week = shift;
    return ($week <= 20)?$week:$week+7;
}

while(<>) {
   if (($degree, $week) = $_ =~ /(\d+)\s(\d+)/) {
        next if ($week == 9 or $week == 10);
        print "$degree ". remap_week($week) . "\n";
   } else {
    print
   }
}

