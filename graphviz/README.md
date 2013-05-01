
Take "pair" files from a pl_archives directory.

Example:

    cat cogent_pairs.txt | ./make-gv.py > all-pairs.gv
    
    dot -oall-pairs-dot.png -Tpng all-pairs.gv
    fdp -Goverlap=prism -oall-pairs-fdp.png -Tpng all-pairs.gv
    sfdp -Goverlap=prism -oall-pairs-sfdp.png -Tpng all-pairs.gv

or

    cat cogent_pairs_matching_hw.txt | ./make-gv.py > matching-pairs.gv

ProTip: edit the "src = " and "dst = " lines in the make-gv.py to get just
the cities, rather than the complete routers (eg, "sfo" instead of "sfo01").
