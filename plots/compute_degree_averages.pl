#!/usr/bin/perl
        
# Computes the average per week of the router degrees.
# select week, average(degree) from degrees group by week order by week
# Input: <degree> <week>
# Output: <week> <average degree>
   
$sum = 0;
$count = 0;     
$last = undef;

print "# week average_degree\n";
while (<>) {
    chomp;
    ($degree, $week) = split;
    next unless defined $week;
    if (defined $last and $last != $week) {
        print $last . " " . $sum/$count . "\n";
        $sum = 0;
        $count = 0;
    }
    $sum += $degree;
    $count ++;
    $last = $week;
}       

print $last . " " . $sum/$count . "\n";
