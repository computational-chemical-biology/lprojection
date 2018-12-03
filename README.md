# lprojection Projection layout for graphs.

# Installation
```
conda create -n lproj python=3.5   
conda install -n lproj rdkit -c rdkit 
source activate lproj
pip install git+https://github.com/mortonjt/minstrel.git
```

If you are getting errors, it is likely because you have garbage channels under your .condarc.  Make sure to delete your .condarc -- you shouldn't need it.

# Getting started

Run the following command to create a projection based layout file gml file colored by compound class. 

```
python layout_script.py \
    -t '4fd90fa52ade4bdcb604945952964fa0,608e5eb3402f4dd599fcc88b1c8a40e9' \
    -p TSNE \
    -w V2 \
    -s 150 \
    -i Cosine \
    -M associated_meta_inchi_match_full.tsv \
    -C superclass_name

```

