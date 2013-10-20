#!/usr/bin/perl

# Remap weeks in router_degree*.dat files
# Skip weeks 9 and 10
# Shift weeks after 20 by 7

sub remap_week {
    my $week = shift;
    return $week if ($week <= 20);
    return $week+7 if ($week <= 22);
    return $week+8;
}

while(<>) {
   if (($degree, $week) = $_ =~ /(\d+)\s(\d+)/) {
        next if ($week == 9 or $week == 10);
        print "$degree ". remap_week($week) . "\n";
   } else {
    print
   }
}

