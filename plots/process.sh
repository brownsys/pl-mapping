export PL_DATA=/research/cogent_map/pl_archives

generateInterfaceBreakdown.py $PL_DATA --allWeeks > iface_breakdown.allweeks.dat
generateInterfaceBreakdown.py $PL_DATA --physical --allWeeks > iface_breakdown.allweeks.physical.dat
generateInterfaceBreakdown.py $PL_DATA --virtual --allWeeks > iface_breakdown.allweeks.virtual.dat

#There's an error in week 10, a shift by one of the interface types
#9	132	2691	6042	140	53	1640	
#10	2737	6082	132	53	1640	140	
#11	137	3153	6260	167	53	2319	


