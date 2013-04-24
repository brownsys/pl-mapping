generateInterfaceBreakdown.py
=============================

Description
------------
Prints out GNUPlot compatible data about the breakdown of interface types (physical vs virtual, etc.) on routers. The script takes in DNS Record data found in "pl_archive/" and options specifying what data you want.

Usage
------
./generateInterfaceBreakdown.py file [options]
file - a COGENT-MASTER-ATLAS.txt file

Options
--------
--allWeeks - Interpret the "file" argument as a directory containing subdirectories labeled with week numbers containing the COGENT-MASTER-ATLAS.txt file for that week. This allows data to be collected across all the weeks. You probably want to pass in "pl_archives/" here.

--physical - Get a breakdown of the physical interfaces in the records. Mutually exclusive with the "--virtual" flag.

--virtual - Get a breakdown of the virtual interfaces in the records. Mutually exclusive with the "--physical" flag.

--normalized - Instead of printing counts, normalize the values so that they are percentages.

NOTE: If neither --physical or --virtual are specified, the script will show a summary of many virtual interfaces and how many physical interfaces there are.

Example
--------

### Get the physical interface breakdown for week 5
./generateInterfaceBreakdown.py pl_archives/5/COGENT-MASTER-ATLAS.txt --physical



### Get the physical vs virtual interface breakdown for all weeks
./generateInterfaceBreakdown.py pl_archives --allWeeks


generateRouterBreakdown.py
=============================

Description
------------
Prints out GNUPlot compatible data about the average degree of routers, disagreement, and router count. The script takes in a directory of data "iffinder-analysis/" and options specifying what data you want.

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
./generateRouterBreakdown.py iffinder-analysis --num-routers --average-degree --disagreement




generateRouterHistogram.py
=============================

Description
------------
Prints out GNUPlot compatible data about the degrees of routers. A single file being analyzed will not bin results for the histogram, but analyzing all weeks will bin the degrees.  The script takes in either a stdout file created by the analyze-iffinder.sh or a directory containing these files such as "iffinder-analysis/".

Usage
------
./generateRouterHistogram.py file
file - the path to the iffinder-analysis directory or a stdout dump in that directory

Example
--------

### Get histogram for a single week
./generateRouterHistogram.py iffinder-analysis/5.stdout.txt

### Get histogram for all weeks
./generateRouterHistogram.py iffinder-analysis
