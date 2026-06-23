library(anpan)
library(ape)

meta_file <- 'metadata.tsv'
tree_file <- 'RAxML_bestTree.t__SGB4933.StrainPhlAn4_sub.tre'

tree <- read.tree(tree_file)
meta <- read.csv(meta_file, header=T, sep='\t')
meta$disease <- factor(meta$disease, levels=c('Control','adenoma', 'CRC', 'carcinoma_surgery_history'))
meta$gender <- factor(meta$sex, levels=c('male','female'))
meta = subset(meta, disease != "carcinoma_surgery_history")
meta = subset(meta, disease != "adenoma")
meta$disease <- factor(meta$disease, levels=c('Control','CRC'))


fit <- anpan_pglmm(meta,
	    tree,
	    outcome = "disease",
	    covariates = c("sex", "age"),
	    omit_na = T,
	    family = "binomial")
