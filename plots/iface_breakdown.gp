set term postscript eps color solid 22 size 5,2.5

set xlabel 'Week'

#Colorbrewer 5 sequential Cool YlGnBu
set style line 1 lc rgbcolor "#253494"
set style line 2 lc rgbcolor "#2C7FB8"
set style line 3 lc rgbcolor "#41B6C4"
set style line 4 lc rgbcolor "#A1DAB4"
set style line 5 lc rgbcolor "#FFFFCC"
#Colorbrewer 5 sequential Warm 
set style line 11 lc rgbcolor "#7A0177"
set style line 12 lc rgbcolor "#C51B8A"
set style line 13 lc rgbcolor "#F768A1"
set style line 14 lc rgbcolor "#FBB4B9"
set style line 15 lc rgbcolor "#FEEBE2"

#border
set border 3
set tics nomirror

# iface by type relative
set output 'iface_breakdown.allweeks.rel.eps'
set ylabel 'Fraction'

set key under  
set style histogram rowstacked gap 2
set boxwidth 1 relative
set style data histograms
set style fill solid 1.0 border lt -1
plot [0.5:] 'iface_breakdown.allweeks.dat' u ($2/($2+$3)):xtic(int($1)%5==0?stringcolumn(1):"") ls 2 t 'Physical', '' u ($3/($2+$3)) ls 5 t 'Virtual'

!epstopdf iface_breakdown.allweeks.rel.eps

# iface by type absolute
set output 'iface_breakdown.allweeks.abs.eps'
set ylabel 'Count (x1000)'

set key under  
set style histogram rowstacked gap 2
set boxwidth 1 relative
set style data histograms
set style fill solid 1.0 border lt -1
plot [0.5:] 'iface_breakdown.allweeks.dat' u ($2/1000):xtic(int($1)%5==0?stringcolumn(1):"") ls 2 t 'Physical', '' u ($3/1000) ls 5 t 'Virtual'

!epstopdf iface_breakdown.allweeks.abs.eps

# physical iface by types breakdown
set output 'iface_breakdown.allweeks.phys-subtypes.abs.eps'
set ylabel 'Count (x1000)'

set key below horizontal 
set style histogram rowstacked gap 2
set boxwidth 1 relative
set style data histograms
set style fill solid 1.0 border lt -1
plot [0.5:] 'iface_breakdown.allweeks.physical.dat' u (($2)/1000):xtic(int($1)%5==0?stringcolumn(1):"") ls 1 t 'POS',\
            '' u ($7/1000) ls 2 t 'Serial',\
            '' u (($5+$6)/1000) ls 3 t '10/100',\
            '' u ($3/1000) ls 4 t '1GigE',\
            '' u ($4/1000) ls 5 t '10GigE'

!epstopdf iface_breakdown.allweeks.phys-subtypes.abs.eps

# virtual iface by types breakdown
set output 'iface_breakdown.allweeks.virt-subtypes.abs.eps'
set ylabel 'Count (x1000)'

set key below horizontal 
set style histogram rowstacked gap 2
set boxwidth 1 relative
set style data histograms
set style fill solid 1.0 border lt -1
plot [0.5:] 'iface_breakdown.allweeks.virtual.dat' u (($2)/1000):xtic(int($1)%5==0?stringcolumn(1):"") ls 11 t 'Tunnel',\
            '' u ($3/1000) ls 12 t 'Multilink',\
            '' u ($5/1000) ls 14 t 'Loopback',\
            '' u (($4)/1000) ls 15 t 'VLAN'

!epstopdf iface_breakdown.allweeks.virt-subtypes.abs.eps


