
##########################################################PCR - patrani #############################
library(curl)
library(httr)
dfP <- data.frame(pid=c("pid"), name=c("name"),born=c("born"),nationality=c("nationality"),features=c("features"))
write.table(dfP, file = "personsData.csv",row.names=FALSE, na="",col.names=FALSE, sep=";")

persons <- readLines("persons.txt")

for(p in persons){
  print(p)
  pids <- unlist(strsplit(p, "=", fixed=TRUE))
  pid <- pids[2]
  page <- readLines( p )
  pageDF <- data.frame(line=page, stringsAsFactors = FALSE)
  name = ""
  born = ""
  nationality = ""
  f = ""
  
  try({
    nameLine <- pageDF[grep("ctl00_ctl00_Application_BasePlaceHolder_lbl_fullName", pageDF$line), "line"]
    nameList <- unlist(strsplit(nameLine, ">", fixed=TRUE))[2]
    name <- unlist(strsplit(nameList, "<", fixed=TRUE))[1]
  }, silent=TRUE)
  
  try({
    bornLine <- pageDF[grep("ctl00_ctl00_Application_BasePlaceHolder_lbl_datumNarozeni", pageDF$line), "line"]
    bornList <- unlist(strsplit(bornLine, ".", fixed=TRUE))[3]
    born <- unlist(strsplit(bornList, "<", fixed=TRUE))[1]
  }, silent=TRUE)
  
  try({
    natLine <- pageDF[grep("ctl00_ctl00_Application_BasePlaceHolder_lbl_Nationality", pageDF$line), "line"]
    natList <- unlist(strsplit(natLine, "(", fixed=TRUE))[2]
    nationality <- unlist(strsplit(natList, ")", fixed=TRUE))[1]
  }, silent=TRUE)
  
  try({
    featuresLine <- pageDF[grep("ctl00_ctl00_Application_BasePlaceHolder_lblDescription", pageDF$line), "line"]
    featuresList <- unlist(strsplit(featuresLine, "<li>", fixed=TRUE))
    features <- c()
    for(f in c(2:length(featuresList))){
      features <- c(features, unlist(strsplit(featuresList[f], "<", fixed=TRUE))[1] )
    }
    f <- paste(features, collapse=',' )
  }, silent=TRUE)
  
  linkLine <- pageDF[grep("<img src=\"ViewImage", pageDF$line), "line"]
  linkList <- unlist(strsplit(linkLine, "\"", fixed=TRUE))[2]
  
  imgLink = paste("http://aplikace.policie.cz/patrani-osoby/", linkList , sep="")
  
  try({
    download.file(imgLink, paste("foto/", pid, ".jpg", sep=""), mode = "wb")
    dfP <- data.frame(pid=c(pid), name=c(name),born=c(born),nationality=c(nationality),features=c(f))
    write.table(dfP, file = "personsData.csv",row.names=FALSE, na="",col.names=FALSE, sep=";", append=TRUE)
  })
    
}



