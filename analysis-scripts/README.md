generateInterfaceBreakdown.py
=============================

Description
------------
Prints out GNUPlot compatible data about the breakdown of interface types
(physical vs virtual, etc.) on routers. The script takes in DNS Record data
found in "pl_archive/" and options specifying what data you want.

Usage
------

    ./generateInterfaceBreakdown.py file [options]
    file - a COGENT-MASTER-ATLAS-FIXED.txt file

Options
--------

    --allWeeks - Interpret the "file" argument as a directory containing
    subdirectories labeled with week numbers containing the
    COGENT-MASTER-ATLAS-FIXED.txt file for that week. This allows data to be
    collected across all the weeks. You probably want to pass in "pl_archives/"
    here.

    --physical - Get a breakdown of the physical interfaces in the records.
    Mutually exclusive with the "--virtual" flag.

    --virtual - Get a breakdown of the virtual interfaces in the records.
    Mutually exclusive with the "--physical" flag.

    --normalized - Instead of printing counts, normalize the values so that
    they are percentages.

NOTE: If neither `--physical` or `--virtual` are specified, the script will
show a summary of many virtual interfaces and how many physical interfaces
there are.

Example
--------

### Get the physical interface breakdown for week 5
    ./generateInterfaceBreakdown.py pl_archives/5/COGENT-MASTER-ATLAS-FIXED.txt --physical
    # POS	GigabitEthernet	TenGigabitEthernet	FastEthernet	Ethernet	Serial	
    137	2830	5784	156	52	2336	

### Get the physical vs virtual interface breakdown for all weeks

    ./generateInterfaceBreakdown.py pl_archives --allWeeks
    # Week	Virtual	Physical	
    1	6263	11165	
    2	6295	11175	
    3	6365	11208	
    4	6394	11262	
    5	6390	11295	
    6	6397	11303	
    7	6382	11285	
    8	6473	11300	
    9	6625	10231	
    10	3924	7069	

generateRouterBreakdown.py
=============================

Description
------------
Prints out GNUPlot compatible data about the average degree of routers,
disagreement, and router count. The script takes in a directory of data
"iffinder-analysis/" and options specifying what data you want.

Usage
------

    ./generateRouterBreakdown.py iffinder_analysis [options]

    iffinder_analysis - the path to the iffinder-analysis directory

Options
--------

    --num-routers - print out the number of routers found that week

    --average-degree - print out the average degree of routers that week

    --disagreement - print out the number of disagreements between iffinder and DNS records that week

NOTE: More than one option may be specified at once.

Example
--------

### Get all information about routers collected

    $ ./generateRouterBreakdown.py iffinder-analysis --num-routers --average-degree --disagreement
    # Week	DisagreementCount	AverageDegree	RouterCount	
    1	38	10.70	2904	
    2	44	10.67	2915	
    3	28	10.73	2895	
    4	28	10.80	2906	
    5	27	10.79	2916	
    6	36	10.81	2908	
    7	38	10.69	2926	
    8	38	10.75	2926	
    9	22	9.99	2962	
    10	17	6.23	1989	

generateRouterHistogram.py
=============================

Description
------------
Prints out GNUPlot compatible data about the degrees of routers. A single file
being analyzed will not bin results for the histogram, but analyzing all weeks
will bin the degrees.  The script takes in either a stdout file created by the
analyze-iffinder.sh or a directory containing these files such as
"iffinder-analysis/".

Usage
------

    ./generateRouterHistogram.py file

    file - the path to the iffinder-analysis directory or a stdout dump in that directory

Example
--------

### Get histogram for a single week

    $ ./generateRouterHistogram.py iffinder-analysis/5.stdout.txt
    # Degree	Count	
    1	535	
    2	126	
    3  	327	
    4	238	
    5	174	
    6	121	
    7	117	
    8	127	
    9	114	
    10	112	

### Get histogram for all weeks

    $ ./generateRouterHistogram.py iffinder-analysis
    # Week	<5	5-10	10-20	20-100	100-300	>300	
    1	1230	644	666	349	15	0	
    2	1235	644	675	346	15	0	
    3	1211	651	667	352	14	0	
    4	1218	649	670	354	15	0	
    5	1226	653	669	353	14	1	
    6	1221	653	663	356	14	1	
    7	1241	657	658	355	14	1	
    8	1230	659	666	356	15	0	
    9	1336	743	576	292	14	1	
    10	1304	365	159	157	4	0	
