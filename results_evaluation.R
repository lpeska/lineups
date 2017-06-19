##########################################################Lineup evaluation #############################
agg_level <- function(resList, dt){
  
  mat <- matrix( 
    0, # the data elements 
    ncol=20,              # number of rows 
    nrow=nrow(dt),              # number of columns 
    byrow = TRUE) 
  i<-1
  for (v in resList){
    v <- as.numeric(v)
    mat[i,v] <- 1
    i <- i+1
  }
  kv <- kripp.alpha(mat, method="nominal")
  kv$value
  
}

res <- read.table("results.csv", header = TRUE, sep=";")
res$relVis = res$visualSelected/res$totalSelected
res$relCB = res$cbSelected/res$totalSelected

res$visualEntries <- as.character(res$visualEntries)
res$cbEntries <- as.character(res$cbEntries)

visList = c()
cbList = c()
for(i in c(1:nrow(res))){
  visList = unlist(c(visList,strsplit(res$visualEntries[i],",")))
  cbList = unlist(c(cbList,strsplit(res$cbEntries[i],",")))
}
visList <- as.numeric(visList)
cbList <- as.numeric(cbList)
mean(visList)
mean(cbList)
sd(visList)
sd(cbList)

dt <- read.table("personsData.csv", header = TRUE, sep=";")

joinedDT <- unique(merge(res, dt, by.x = "lineupID", by.y = "pid"))

outerRegions <- joinedDT[ which(!(joinedDT$nationality %in% c("CZ", "SK", "H"))),]
innerRegions <- joinedDT[ which(joinedDT$nationality %in% c("CZ", "SK", "H")),]

visList = c()
cbList = c()
for(i in c(1:nrow(outerRegions))){
  visList = unlist(c(visList,strsplit(outerRegions$visualEntries[i],",")))
  cbList = unlist(c(cbList,strsplit(outerRegions$cbEntries[i],",")))
}
visList <- as.numeric(visList)
cbList <- as.numeric(cbList)
mean(visList)
mean(cbList)

visList = c()
cbList = c()
for(i in c(1:nrow(innerRegions))){
  visList = unlist(c(visList,strsplit(innerRegions$visualEntries[i],",")))
  cbList = unlist(c(cbList,strsplit(innerRegions$cbEntries[i],",")))
}
visList <- as.numeric(visList)
cbList <- as.numeric(cbList)
mean(visList)
mean(cbList)

lv <- c()
lc <- c()
res$lineupID <- as.factor(res$lineupID)
for(l in unique(res$lineupID)){
  d <- res[which(res$lineupID == l),]

  cbList = strsplit(d$cbEntries,",")
  visList = strsplit(d$visualEntries,",")
  
  kv <- agg_level(visList, d)
  kc <- agg_level(cbList, d)
  
  lv <- c(unlist(lv), kv)
  lc <- c(unlist(lc), kc)
}
mean(lc)
mean(lv)


lv <- c()
lc <- c()
outerRegions$lineupID <- as.factor(outerRegions$lineupID)
for(l in unique(outerRegions$lineupID)){
  d <- outerRegions[which(outerRegions$lineupID == l),]
  
  cbList = strsplit(d$cbEntries,",")
  visList = strsplit(d$visualEntries,",")
  
  kv <- agg_level(visList, d)
  kc <- agg_level(cbList, d)
  
  lv <- c(unlist(lv), kv)
  lc <- c(unlist(lc), kc)
}
mean(lc)
mean(lv)

plot(res$relVis~res$lineupID,  las = 2)
plot(res$relCB~res$lineupID,  las = 2)

table(joinedDT$nationality)

table(res$lineupID)
table(res$evaluatorName)

mean(res$totalSelected)
mean(res$visualSelected)
mean(res$cbSelected)
mean(res$bothSelected)

sd(res$totalSelected)
sd(res$visualSelected)
sd(res$cbSelected)
sd(res$bothSelected)

sum(res$totalSelected)
sum(res$visualSelected)
sum(res$cbSelected)
sum(res$bothSelected)

sum(innerRegions$totalSelected)
sum(innerRegions$visualSelected)
sum(innerRegions$cbSelected)
sum(innerRegions$bothSelected)

sum(outerRegions$totalSelected)
sum(outerRegions$visualSelected)
sum(outerRegions$cbSelected)
sum(outerRegions$bothSelected)


mean(res$relVis)
mean(res$relCB)

sd(res$relVis)
sd(res$relCB)

t.test(res$visualSelected, res$cbSelected, paired = TRUE)
t.test(innerRegions$visualSelected, innerRegions$cbSelected, paired = TRUE)
t.test(outerRegions$visualSelected, outerRegions$cbSelected, paired = TRUE)

t.test(innerRegions$relVis, innerRegions$relCB, paired = TRUE, alt="greater")
t.test(outerRegions$relVis, outerRegions$relCB, paired = TRUE)
t.test(outerRegions$visualSelected, outerRegions$cbSelected, paired = TRUE)


t.test(res$relVis, res$relCB, paired = TRUE, alt="greater")
t.test(innerRegions$relVis, innerRegions$relCB, paired = TRUE, alt="greater")
t.test(outerRegions$relVis, outerRegions$relCB, paired = TRUE)
t.test(outerRegions$visualSelected, outerRegions$cbSelected, paired = TRUE)





