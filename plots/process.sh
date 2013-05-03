export PL_DATA=/research/cogent_map/pl_archives
export IFFINDER=/research/cogent_map/iffinder-analysis
export PL_BIN=$HOME/projects/pl-mapping/analysis-scripts

#Files needed by iface_breakdown.gp
$PL_BIN/generateInterfaceBreakdown.py $PL_DATA --allWeeks > iface_breakdown.allweeks.dat
$PL_BIN/generateInterfaceBreakdown.py $PL_DATA --physical --allWeeks > iface_breakdown.allweeks.physical.dat
$PL_BIN/generateInterfaceBreakdown.py $PL_DATA --virtual --allWeeks > iface_breakdown.allweeks.virtual.dat

#Files needed by router_degrees.gp
$PL_BIN/generateRouterHistogram.py $IFFINDER $PL_DATA > router_degrees.all.dat
$PL_BIN/generateRouterHistogram.py $IFFINDER $PL_DATA --physical > router_degrees.physical.dat
$PL_BIN/generateRouterHistogram.py $IFFINDER $PL_DATA --virtual > router_degrees.virtual.dat

cat router_degrees.all.dat | perl compute_degree_averages.pl  > router_degrees.all.avg.dat
cat router_degrees.physical.dat | perl compute_degree_averages.pl  > router_degrees.physical.avg.dat
cat router_degrees.virtual.dat | perl compute_degree_averages.pl  > router_degrees.virtual.avg.dat



