library(ggplot2)
setwd('/home/enrico/Dropbox/SFEM/validation/FEIII2016/')
#results_0.1 <- read.csv('performance_fraction_0.1.csv')
#results_0.2 <- read.csv('performance_fraction_0.2.csv')
#results_0.3 <- read.csv('performance_fraction_0.3.csv')
#results_0.4 <- read.csv('performance_fraction_0.4.csv')
#results_0.5 <- read.csv('performance_fraction_0.5.csv')
#results_0.6 <- read.csv('performance_fraction_0.6.csv')
#results_0.7 <- read.csv('performance_fraction_0.7.csv')
#results_0.8 <- read.csv('performance_fraction_0.8.csv')
#results_0.9 <- read.csv('performance_fraction_0.9.csv')
#p1<-results_0.1['f']$f
#p2<-results_0.2['f']$f
#p3<-results_0.3['f']$f
#p4<-results_0.4['f']$f
#p5<-results_0.5['f']$f
#p6<-results_0.6['f']$f
#p7<-results_0.7['f']$f
#p8<-results_0.8['f']$f
#p9<-results_0.9['f']$f

data <- read.csv('sfem_validation_results.csv')

#list of f-score with 0.1 of the gold standard
F1 <- data[data$frac == 0.1,]$F
F2 <- data[data$frac == 0.2,]$F
F3 <- data[data$frac == 0.3,]$F
F4 <- data[data$frac == 0.4,]$F
F5 <- data[data$frac == 0.5,]$F
F6 <- data[data$frac == 0.6,]$F
F7 <- data[data$frac == 0.7,]$F
F8 <- data[data$frac == 0.8,]$F
F9 <- data[data$frac == 0.9,]$F

m1 = mean(F1)
m2 = mean(F2)
m3 = mean(F3)
m4 = mean(F4)
m5 = mean(F5)
m6 = mean(F6)
m7 = mean(F7)
m8 = mean(F8)
m9 = mean(F9)


min1 = min(F1)
min2 = min(F2)
min3 = min(F3)
min4 = min(F4)
min5 = min(F5)
min6 = min(F6)
min7 = min(F7)
min8 = min(F8)
min9 = min(F9)

max1 = max(F1)
max2 = max(F2)
max3 = max(F3)
max4 = max(F4)
max5 = max(F5)
max6 = max(F6)
max7 = max(F7)
max8 = max(F8)
max9 = max(F9)
#max10 = max(p10)

pointstoplot<-c(m1,m2,m3,m4,m5,m6,m7,m8,m9)

s1 = sd(p1)
s2 = sd(p2)
s3 = sd(p3)
s4 = sd(p4)
s5 = sd(p5)
s6 = sd(p6)
s7 = sd(p7)
s8 = sd(p8)
s9 = sd(p9)
#s10 = sd(p10)

indexes<-c(10,20,30,40,50,60,70,80,90)
sds<-c(s1,s2,s3,s4,s5,s6,s7,s8,s9)
mins<-c(min1,min2,min3,min4,min5,min6,min7,min8,min9)
maxes<-c(max1,max2,max3,max4,max5,max6,max7,max8,max9)
up_bound <- c(m1+s1,m2+s2,m3+s3,m4+s4,m5+s5,m6+s6,m7+s7,m8+s8,m9+s9)
low_bound <- c(m1-s1,m2-s2,m3-s3,m4-s4,m5-s5,m6-s6,m7-s7,m8-s8,m9-s9)
x = cbind(data.frame(indexes,pointstoplot, sds, low_bound, up_bound))

qplot(x=indexes, y=pointstoplot, xlab="Percentage of Training Data Used", ylab="F-Measure") + geom_errorbar(aes(ymin=low_bound, ymax=up_bound))

#estimating the growth speed with a linear fit
indexes_fit <- indexes/100 #rescale to 0-1
fit <- lm(pointstoplot ~ indexes_fit, weights = 1/sds**2) #setting the estimated variances as errors 
summary(fit)

