
export PL_DATA=/research/cogent_map/pl_archives
export IFFINDER=/research/cogent_map/iffinder-analysis
export PL_BIN=$HOME/work/projects/pl-mapping/analysis-scripts

# !!! REQUIRES GNUPLOT v 4.6 or higher
gnuplot --version | awk '{if ($2 >= 4.6) exit 0}'
status=$?
if [ $status -ne 0 ]; then
    echo "Must use gnuplot v 4.6 or higher"
    exit 1
fi

#Files needed by iface_breakdown.gp
$PL_BIN/generateInterfaceBreakdown.py $PL_DATA --allWeeks > iface_breakdown.allweeks.dat
$PL_BIN/generateInterfaceBreakdown.py $PL_DATA --physical --allWeeks > iface_breakdown.allweeks.physical.dat
$PL_BIN/generateInterfaceBreakdown.py $PL_DATA --virtual --allWeeks > iface_breakdown.allweeks.virtual.dat

gnuplot iface_breakdown.gp

#Files needed by router_degrees.gp
$PL_BIN/generateRouterHistogram.py $IFFINDER $PL_DATA > router_degrees.all.dat
$PL_BIN/generateRouterHistogram.py $IFFINDER $PL_DATA --physical > router_degrees.physical.dat
$PL_BIN/generateRouterHistogram.py $IFFINDER $PL_DATA --virtual > router_degrees.virtual.dat

cat router_degrees.all.dat | perl compute_degree_averages.pl  > router_degrees.all.avg.dat
cat router_degrees.physical.dat | perl compute_degree_averages.pl  > router_degrees.physical.avg.dat
cat router_degrees.virtual.dat | perl compute_degree_averages.pl  > router_degrees.virtual.avg.dat

gnuplot router_degrees.gp

rm *.eps

