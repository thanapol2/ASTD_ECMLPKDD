library('fma')
library("jsonlite")

rm(list = ls())

# Fig 1a : walkJog
setwd('dataset/02_Real1_datasets')
FILE_NAME <- '01_WalkJogRun1.json'
json_data <- fromJSON(txt = FILE_NAME)
ts_data <- json_data$ts
par(mar = c(4.2, 5, 1, 1),cex.lab = 2, cex.axis = 2) 
plot(ts_data,type='l',
     xlab="timestamp", ylab="Angular velocity",xlim=c(3100, 4100)
)
abline(v=3800, col=adjustcolor("red", alpha = 0.7), lty=2, lwd=3)

# Fig 1b : lynx
par(mar = c(4.2, 5, 1, 1),cex.lab = 2, cex.axis = 2)   
plot(lynx,
     xlab="Year", ylab="Popluation",xlim=c(1830, 1880)
     )

abline(v=1860, col=adjustcolor("red", alpha = 0.7), lty=2, lwd=3)
abline(v=1870, col=adjustcolor("red", alpha = 0.7), lty=2, lwd=3)