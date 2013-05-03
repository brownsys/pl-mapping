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
"iffinder-analysis/", a directory of DNS records "pl_archives/",  and
options specifying what data you want.

Usage
------

    ./generateRouterBreakdown.py iffinder_analysis pl_archives [options]

    iffinder_analysis - the path to the iffinder-analysis directory
    pl_archives - the path to the pl_archives directory

Options
--------

    --num-routers - print out the number of routers found that week

    --average-degree - print out the average degree of routers that week (only takes into account physical interfaces)

    --disagreement - print out the number of disagreements between iffinder and DNS records that week

NOTE: More than one option may be specified at once.

Example
--------

### Get all information about routers collected

    $ ./generateRouterBreakdown.py iffinder-analysis pl_archives --num-routers --average-degree --disagreement
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
Prints out GNUPlot compatible data about the degrees of routers.
The script takes in either a stdout file created by the
analyze-iffinder.sh or a directory containing these files such as
"iffinder-analysis/" and the "pl_archives/" directory for DNS record lookup.

Usage
------

    ./generateRouterHistogram.py file pl_archives [OPTIONS]

    file - the path to the iffinder-analysis directory or a stdout dump in that directory
    pl_archives - the path to the pl_archives directory containing DNS records

Options
--------

    --physical - print numbers only in terms of physical interfaces

    --virtual - print numbers only in terms of virtual interfaces

Example
--------

### Get histogram for a single week

    $ ./generateRouterHistogram.py iffinder-analysis/5.stdout.txt pl_archives
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

    $ ./generateRouterHistogram.py iffinder-analysis pl_archives
    # Degree    Week
    1    1
    1    1
    192    2

getNewPhysicalInterfaces.py
=============================

Description
------------
Prints out GNUPlot compatible data about the number of new physical interfaces found in a week. 
A new interface is one that did not appear in the week before as a physical interface or at all.
This number is trustworthy because we have already smoothed the data to remove DNS errors.

Usage
------

    ./getNewPhysicalInterfaces.py pl_archives [weekNumbers]

    pl_archives - The "pl_archives/" directory
    weekNumbers - a set of weeks you are interested in

Example
--------

### Get new interface count

    $ ./getNewPhysicalInterfaces.py pl_archives
    # Week	NumNewPhyInterfaces
    2	106
    3	201
    4	199
    5	108
    6	109
    7	79
    8	199
    9	1356
    10	1472
    11	16787
    12	76
    13	116

