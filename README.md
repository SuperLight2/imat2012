Some hints with command shell

1. When you have test set with features (id is the first column) and calculate probabilities of switch (in file probability.tsv)
for each line, then you can make resulting file using next commands

cat test_features.tsv|cut -f 1|paste - probability.tsv|sort -k 2 -gr|cut -f 1 > result.tsv
cat test_features.tsv|cut -f 1|paste - probability.tsv|sort -k 2 -gr|cut -f 1|gzip -c > result.tsv.gz

2. If you want to calc auc for some validate set you need file with probabilities of switch (in file probability.tsv).
Then you can use calc_auc.py script:

cat validate_features.tsv|cut -f 2|paste - probability.tsv|sort -k 2 -gr|cut -f 1|python calc_auc.py