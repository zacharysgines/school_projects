library(biotools)

###Read in data
AL1 <- read.csv("C:/School/Multivariate/FinalProject/AL_Data_2013_2021.csv", fileEncoding="UTF-8-BOM"); head(AL1)
NL1 <- read.csv("C:/School/Multivariate/FinalProject/NL_Data_2013_2021.csv", fileEncoding="UTF-8-BOM"); head(NL1)
AL2 <- read.csv("C:/School/Multivariate/FinalProject/AL_Data_2022.csv", fileEncoding="UTF-8-BOM"); head(AL2)
NL2 <- read.csv("C:/School/Multivariate/FinalProject/NL_Data_2022.csv", fileEncoding="UTF-8-BOM"); head(NL2)
AL1 <- cbind(AL1[,c(-5, -6, -7)], Class = "AL1")
NL1 <- cbind(NL1[,c(-5, -6, -7)], Class = "NL1")
AL2 <- cbind(AL2[,c(-5, -6, -7)], Class = "AL2")
NL2 <- cbind(NL2[,c(-5, -6, -7)], Class = "NL2")
Full_Data <- rbind(AL1, AL2, NL1, NL2)

###Plot data to look for normality and outliers
plot(Full_Data[,6], Full_Data[,7], xlab = "Batting Average", ylab = "On Base Percentage")
plot(Full_Data[,6], Full_Data[,8], xlab = "Batting Average", ylab = "Slugging Percentage")
plot(Full_Data[,7], Full_Data[,8], xlab = "On Base Percentage", ylab = "Slugging Percentage")

###Identify and remove outliers
outliers <- Full_Data[Full_Data$SLG > .85 | Full_Data$BA > .35 | Full_Data$OBP > .45,]
data <- Full_Data[Full_Data$BA <= .35 & Full_Data$OBP <= .45 & Full_Data$SLG <= .85,]

###Plot data without outliers
plot(data[,6], data[,7], xlab = "Batting Average", ylab = "On Base Percentage")
plot(data[,6], data[,8], xlab = "Batting Average", ylab = "Slugging Percentage")
plot(data[,7], data[,8], xlab = "On Base Percentage", ylab = "Slugging Percentage")

###Identify correlation between variables
cor(data[,6], data[,7])
cor(data[,6], data[,8])
cor(data[,7], data[,8])

###Split data into groups by league and year
groups <- split(data[,-9], data[,9])
AL1 <- groups$AL1
NL1 <- groups$NL1
AL2 <- groups$AL2
NL2 <- groups$NL2

###Analyze mean and standard deviation of each group and of the overall data
###and find variance-covariance matrices
mean(AL1$BA); mean(NL1$BA); mean(AL2$BA); mean(NL2$BA); mean(data$BA)
mean(AL1$OBP); mean(NL1$OBP); mean(AL2$OBP); mean(NL2$OBP); mean(data$OBP)
mean(AL1$SLG); mean(NL1$SLG); mean(AL2$SLG); mean(NL2$SLG); mean(data$SLG)
sd(AL1$BA); sd(NL1$BA); sd(AL2$BA); sd(NL2$BA); sd(data$BA)
sd(AL1$OBP); sd(NL1$OBP); sd(AL2$OBP); sd(NL2$OBP); sd(data$OBP)
sd(AL1$SLG); sd(NL1$SLG); sd(AL2$SLG); sd(NL2$SLG); sd(data$SLG)
sigma1 <- cov(AL1[,6:8])
sigma2 <- cov(NL1[,6:8])
sigma3 <- cov(AL2[,6:8])
sigma4 <- cov(NL2[,6:8])

###Test for equality of variance-covariance matrices
boxM(data[,6:8], data[,9])

###Test for equality of variance between AL1 and NL1
data_13_to_21 <- rbind(data[data$Class == "AL1", 6:9], data[data$Class == "NL1", 6:9])
boxM(data_13_to_21[,-4], data_13_to_21[,4])

###Test for equality of variance between AL2 and NL2
data_22 <- rbind(data[data$Class == "AL2", 6:9], data[data$Class == "NL2", 6:9])
boxM(data_22[,-4], data_22[,4])

###Test for equality of variance between NL1 and NL2
NL_data <- rbind(data[data$Class == "NL1", 6:9], data[data$Class == "NL2", 6:9])
boxM(NL_data[,-4], NL_data[,4])


###T2 test for AL vs. NL (2013-2021)
AL <- AL1[,6:8]
NL <- NL1[,6:8]
x1bar <- colMeans(AL); x1bar
x2bar <- colMeans(NL); x2bar
s1 <- cov(AL); s1
s2 <- cov(NL); s2
n1 <- nrow(AL); n1
n2 <- nrow(NL); n2
p <- ncol(AL); p
alpha <- .05

#Find test statistic, crit value and compare
t2 <- t(x1bar-x2bar)%*%solve(((1/n1)*s1)+((1/n2)*s2))%*%(x1bar-x2bar); t2
crit_val <- qchisq(alpha, p, lower.tail = F); crit_val
t2 > crit_val

###T2 test for AL vs. NL (2022)
AL <- AL2[,6:8]
NL <- NL2[,6:8]
x1bar <- colMeans(AL); x1bar
x2bar <- colMeans(NL); x2bar
s1 <- cov(AL); s1
s2 <- cov(NL); s2
n1 <- nrow(AL); n1
n2 <- nrow(NL); n2
p <- ncol(AL); p
alpha <- .05

#Find test statistic, crit value and compare
sp <- ((n1-1)*s1+(n2-1)*s2)/(n1+n2-2)
t2 <- t(x1bar-x2bar)%*%solve((1/n1+1/n2)*sp)%*%(x1bar-x2bar); t2
crit_val <- ((n1+n2-2)/(n1+n2-p-1))*qf(alpha, p, (n1+n2-p-1), lower.tail = F); crit_val
t2 > crit_val

###T2 test for NL Comparison
NL_1 <- NL1[,6:8]
NL_2 <- NL2[,6:8]
x1bar <- colMeans(NL_1); x1bar
x2bar <- colMeans(NL_2); x2bar
s1 <- cov(NL_1); s1
s2 <- cov(NL_2); s2
n1 <- nrow(NL_1); n1
n2 <- nrow(NL_2); n2
p <- ncol(NL_1); p
alpha <- .05

#Find test statistic, crit value and compare
t2 <- t(x1bar-x2bar)%*%solve(((1/n1)*s1)+((1/n2)*s2))%*%(x1bar-x2bar); t2
crit_val <- qchisq(alpha, p, lower.tail = F); crit_val
t2 > crit_val

###Simultaneous confidence intervals for NL1 vs. AL1
AL <- AL1[,6:8]
NL <- NL1[,6:8]
x1bar <- colMeans(AL); x1bar
x2bar <- colMeans(NL); x2bar
s1 <- cov(AL); s1
s2 <- cov(NL); s2
p <- ncol(AL); p
alpha <- .05

CI <- matrix(nrow = p, ncol = 2)
chi <- qchisq(alpha, p, lower.tail = F)
c <- 1/n1*s1+1/n2*s2

for (i in 1:p){
  CI[i, 1] <- (x1bar[i]-x2bar[i])-(sqrt(chi)*sqrt(c[i,i]))
  CI[i, 2] <- (x1bar[i]-x2bar[i])+(sqrt(chi)*sqrt(c[i,i]))
}; CI

###Simultaneous confidence intervals for NL1 vs. AL1
NL_1 <- NL1[,6:8]
NL_2 <- NL2[,6:8]
x1bar <- colMeans(NL_1); x1bar
x2bar <- colMeans(NL_2); x2bar
s1 <- cov(NL_1); s1
s2 <- cov(NL_2); s2
p <- ncol(NL_1); p
alpha <- .05

CI <- matrix(nrow = p, ncol = 2)
chi <- qchisq(alpha, p, lower.tail = F)
c <- 1/n1*s1+1/n2*s2

for (i in 1:p){
  CI[i, 1] <- (x1bar[i]-x2bar[i])-(sqrt(chi)*sqrt(c[i,i]))
  CI[i, 2] <- (x1bar[i]-x2bar[i])+(sqrt(chi)*sqrt(c[i,i]))
}; CI

