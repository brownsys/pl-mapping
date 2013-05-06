set term postscript eps color solid size 5,2.5 22
set border 2 front linetype -1 linewidth 1.000

set boxwidth 0.8 absolute
set bars 0.5
set style fill solid 0.25 border lt -1
set style boxplot fraction 0.99

unset key
set pointsize 0.2

set xtics border in scale 0,0 nomirror norotate  offset character 0, 0, 0 autojustify
set xtics 5
set ytics nomirror

set xrange [0:53]

set logscale y

set xlabel 'Week'

#plot 'router_degrees.all' u (1):1:(0):2 w boxplot

set output 'router_degrees.all.eps'
set yrange [1:400]
set ylabel 'All Interfaces per Router'
plot for [i=0:52] 'router_degrees.all.dat' u 2:1:(0) index i  w boxplot lc 3,\
     'router_degrees.all.avg.dat' u 1:2:2:2:2 w candlesticks lw 4 lc 1
!epstopdf router_degrees.all.eps

set output 'router_degrees.physical.eps'
set yrange [1:200]
set ylabel 'Physical Interfaces per Router'
plot for [i=0:52] 'router_degrees.physical.dat' u 2:1:(0) index i  w boxplot lc 3,\
     'router_degrees.physical.avg.dat' u 1:2:2:2:2 w candlesticks lw 4 lc 1
!epstopdf router_degrees.physical.eps

set output 'router_degrees.virtual.eps'
set yrange [1:400]
set ylabel 'Virtual Interfaces per Router'
plot for [i=0:52] 'router_degrees.virtual.dat' u 2:1:(0) index i  w boxplot lc 3,\
     'router_degrees.virtual.avg.dat' u 1:2:2:2:2 w candlesticks lw 4 lc 1
!epstopdf router_degrees.virtual.eps
