
args <- commandArgs(trailingOnly = TRUE)

if (length(args) != 4) {
    stop("incorrect arguments! Must be <train file> <test file> <test prediction file> <train prediction file>")
}

library("gbm")

set.seed(20286298)

train.tsv = read.csv(args[1], header=FALSE, sep = "\t")
test.tsv = read.csv(args[2], header=FALSE, sep = "\t")

XTRAIN = as.matrix(train.tsv[, c(-1, -2)])
YTRAIN = as.matrix(train.tsv[, 2])
XTEST = as.matrix(test.tsv[, c(-1, -2)])

rows_train = length(XTRAIN[,1])
rows_test = length(XTEST[,1])
ncol_train = length(XTRAIN[1,])

trees_count = 3000
learn_elements_count = 500000

result = numeric(rows_test)
result_train = numeric(rows_train)

outer_iter = 20

for (l in 1 : outer_iter) {

    rows = sample(1 : rows_train, learn_elements_count)
    cols_count = sample(ncol_train - 3 : ncol_train, 1)
    cols = sample(1 : ncol_train, cols_count)

    XLEARN = XTRAIN[rows, ]
    YLEARN = YTRAIN[rows, ]

    model = gbm.fit(XLEARN, YLEARN,
                    offset = NULL,
                    misc = NULL,
                    distribution = "bernoulli",
                    n.trees = trees_count,
                    interaction.depth = 10,
                    n.minobsinnode = 15,
                    shrinkage = 0.02,
                    bag.fraction = 0.5,
                    var.monotone = NULL,
                    keep.data = TRUE,
                    verbose = TRUE)

    new_result = predict.gbm(model,
                             XTEST,
                             n.trees = trees_count,
                             type = "response")
    
    result = result + new_result

    new_result = predict.gbm(model,
                             XTRAIN,
                             n.trees = trees_count,
                             type = "response")

    result_train = result_train + new_result
}

result = result / outer_iter
result_train = result_train / outer_iter

write.table(matrix(c(XTEST[,1], result), ncol = 2), sep = "\t", args[3], row.names=FALSE, col.names=FALSE)

write.table(matrix(c(XTRAIN[,1], result_train), ncol = 2), sep = "\t", args[4], row.names=FALSE, col.names=FALSE)
