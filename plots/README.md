These scripts generate the data used to make the plots in the imc paper.
The process.sh script does all that is needed, and places data in the
gen-data directory.

Copy those files to the support/plots directory of the paper repository.


Notes:
* If there is a gap in weeks
 * adjust fix_weeks_router_degrees.pl
 * adjust fix_weeks_iface_breakdown.pl
 * adjust transpose_summaries.pl
 ( I know, these remap_week functions are identical and should be in one place. Oh well)
There currently are two gaps:
  week 21 -> 28
  week 30 (already corrected) -> 31

Description for the Router Degrees graphs:

Modified boxplots showing the distribution of router degrees in our dataset over successive weeks.
The boxes cover the second to third quartiles, and the whiskers range from minimum to maximum.
with outliers shown as dots. The thin horizontal line inside the boxes is the median, and
the thicker horizontal line the mean. The distribution is heavily concentrated on smaller
degrees, and remains fairly stable over time.




