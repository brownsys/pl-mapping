set term postscript eps color solid 22 size 5,2.5

set xlabel 'Week'

#Colorbrewer 5 sequential Cool YlGnBu
set style line 1 lc rgbcolor "#0C2C84"
set style line 2 lc rgbcolor "#225EA8"
set style line 3 lc rgbcolor "#1D91C0"
set style line 4 lc rgbcolor "#41B6C4"
set style line 5 lc rgbcolor "#7FCDBB"
set style line 6 lc rgbcolor "#C7E9B4"
set style line 7 lc rgbcolor "#FFFFCC"
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

# Week	Ethernet	FastEthernet	GigabitEthernet	IntegratedServicesModule	POS	Serial	TenGigabitEthernet	
# 1     2           3               4               5                           6   7       8
#       *                                           *                           * 
# Add '*' to others
plot [0.5:] 'iface_breakdown.allweeks.physical.dat' u (($7)/1000):xtic(int($1)%5==0?stringcolumn(1):"") ls 1 t 'Serial',\
            '' u ($3/1000) ls 4 t 'FastEth',\
            '' u ($4/1000) ls 5 t '1GigE',\
            '' u ($8/1000) ls 6 t '10GigE',\
            '' u (($6+$2+$5)/1000) ls 7 t 'Others'

!epstopdf iface_breakdown.allweeks.phys-subtypes.abs.eps

#set logscale y
set term postscript eps color 22 size 5,2.5 dashed
set output 'iface_breakdown.allweeks.phys-subtypes.steps.eps'
plot [0.5:] 'iface_breakdown.allweeks.physical.dat' u (($3)/1000):xtic(int($1)%5==0?stringcolumn(1):"") w steps lw 4 t 'FastEth',\
            '' u ($8/1000) w steps lw 4 t '10GigE',\
            '' u ($4/1000) w steps lw 4 t '1GigE',\
            '' u ($7/1000) w steps lw 4 t 'Serial',\
            '' u ($2/1000) w steps lw 4 t 'Eth',\
            '' u ($5/1000) w steps lw 4 t 'ISM',\
            '' u ($6/1000) w steps lw 4 t 'POS'

!epstopdf iface_breakdown.allweeks.phys-subtypes.steps.eps
unset logscale y


# virtual iface by types breakdown
set term postscript eps color solid 22 size 5,2.5
set output 'iface_breakdown.allweeks.virt-subtypes.abs.eps'
set ylabel 'Count (x1000)'

set key below horizontal 
set style histogram rowstacked gap 2
set boxwidth 1 relative
set style data histograms
set style fill solid 1.0 border lt -1

# Week	Loopback	Multilink	Tunnel	Vlan	
# 1     2           3           4       5
plot [0.5:] 'iface_breakdown.allweeks.virtual.dat' u (($4)/1000):xtic(int($1)%5==0?stringcolumn(1):"") ls 11 t 'Tunnel',\
            '' u ($3/1000) ls 12 t 'Multilink',\
            '' u ($2/1000) ls 14 t 'Loopback',\
            '' u ($5/1000) ls 15 t 'VLAN'

!epstopdf iface_breakdown.allweeks.virt-subtypes.abs.eps


