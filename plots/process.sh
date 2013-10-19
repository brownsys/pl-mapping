# This file processes the raw data in $PL_DATA and generates data files that
# we use to plot them in the imc13 paper. It lives in the pl-mapping git repo.
# The data files produced are then plotted using the gnuplot scripts in the
# paper repo.
# The files produced in the gen-data directory should be copied over to the
# paper repository.
export PL_DATA=/research/cogent_map/pl_archives
export IFFINDER=/research/cogent_map/iffinder-analysis
export PL_BIN=$HOME/work/projects/pl-mapping/analysis-scripts

mkdir gen-data

#File required by dns-results.gp
./transpose-summaries.pl $PL_DATA > gen-data/summary-transpose.txt

#Files needed by iface_breakdown.gp
$PL_BIN/generateInterfaceBreakdown.py $PL_DATA --allWeeks > gen-data/iface_breakdown.allweeks.dat
$PL_BIN/generateInterfaceBreakdown.py $PL_DATA --physical --allWeeks > gen-data/iface_breakdown.allweeks.physical.dat
$PL_BIN/generateInterfaceBreakdown.py $PL_DATA --virtual --allWeeks > gen-data/iface_breakdown.allweeks.virtual.dat

#gnuplot iface_breakdown.gp

#Files needed by router_degrees.gp
$PL_BIN/generateRouterHistogram.py $IFFINDER $PL_DATA > gen-data/router_degrees.all.dat
$PL_BIN/generateRouterHistogram.py $IFFINDER $PL_DATA --physical > gen-data/router_degrees.physical.dat
$PL_BIN/generateRouterHistogram.py $IFFINDER $PL_DATA --virtual > gen-data/router_degrees.virtual.dat


#Remap weeks and remove weeks 9 and 10
cat gen-data/router_degrees.all.dat | ./fix_weeks_router_degrees.pl > gen-data/router_degrees.fixed.all.dat
cat gen-data/router_degrees.physical.dat | ./fix_weeks_router_degrees.pl > gen-data/router_degrees.fixed.physical.dat
cat gen-data/router_degrees.virtual.dat | ./fix_weeks_router_degrees.pl > gen-data/router_degrees.fixed.virtual.dat

#Compute the average degree for each week
cat gen-data/router_degrees.fixed.all.dat | perl compute_degree_averages.pl  > gen-data/router_degrees.fixed.all.avg.dat
cat gen-data/router_degrees.fixed.physical.dat | perl compute_degree_averages.pl  > gen-data/router_degrees.fixed.physical.avg.dat
cat gen-data/router_degrees.fixed.virtual.dat | perl compute_degree_averages.pl  > gen-data/router_degrees.fixed.virtual.avg.dat

#Normalize the CDFs
./normalize.pl gen-data/router_degrees.fixed.all.dat
./normalize.pl gen-data/router_degrees.fixed.physical.dat
./normalize.pl gen-data/router_degrees.fixed.virtual.dat

#gnuplot router_degrees.gp

rm *.eps

