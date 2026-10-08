friends <- c("JUNE", "MolayO", "RasheedaT", "Louis","Victor")
age <- c(26, 40, 27, 25, 21)
a <- age[1] + age[3]/3
round(a, 15)

name_lower = tolower(friends)
name_lower

elemenet_upper = toupper(friends[2])
elemenet_upper


#3nota <- 2.1
x <- round(x, 5)
x


haba <- letters(friends)
haba
help("letters")

for (x in 1:10) {
  print(x ,sep="\n")
}

cat(paste(x, collapse = "\n"), "\n")


help(package ='stats')
help.search("lower")

apropos('lower', mode="function")

help("lower.tri")


m2 <- matrix(1:20, 4, 5)
lower.tri(m2)
m2


m3 <- matrix(1:20, 4, 5)

install.packages("ggplot2")
library(ggplot2)


lsf.str("package:ggplot2")
ls("package:ggplot2")

# If FALSE, install the pac
if (require("ggplot2")) {
  print(TRUE)
} else if (library("tidiverse")) {
  print(FALSE)
}

if (require("ggplot2")) {
  print(TRUE)
} else if (require("tidyverse")) {
  print(FALSE)
}


noms <- c("Alice", "Bob", "Charlie")

for (nom in noms) {
  print(nom)
}
z <- c(12, 15, 3, 22)
sort(z)
z[order(-z)]




#verify the data type of the element or vector or converted data type 
#is.character()  # as.character()
# is.numeric()   # as.numeric()
# is.logical()  # as.logical()
# is.integer()  # as.integer()
#

### find the data type of element in the vector 
### typeof()
### class()

##
x <- c('a', 'b', 'c', 'd')
is.character(x)

Z <- c(1.3, pi, 4)
is.numeric(Z)

######################################
rm(list=ls())  


ch <- c("YES", "NO", "YES", "YES", "NO", "YES", "YES")
as.factor(ch)


X <- c("A", "B", "A")
factor(X, levels=c("A", "B"))


Zi <- LETTERS[3:1]
Zi
name <- factor(Zi, ordered = TRUE)
name
attributes(name)


help("attributes")


g <- c(1,2,1,2)
factor(g, levels = c(1,2), labels = c("M", "F"))


help(factor)


factor(x = character(),         # Input vector data
       levels,                  # Input of unique x values (optional)
       labels = levels,         # Output labels for the levels (optional)
       exclude = NA,            # Values to be excluded from levels
       ordered = is.ordered(x), # Whether the input levels are ordered as given or not
       nmax = NA)      # Maximum number of levels

x <- -2:2
x



vect <- c(1L:5L)
vect[-2L]
vect
vect_1 <- c(10L:15L)
vect_1


x <- c(10, 20, 30)
class(x)


x <- c(1, TRUE, 3L , 3+5i)
class(x)


x <- c(100, 200, 300)
as.character(x)


genre <- c('Romance', 'Scifi', 'Comedy', 'Thriller')
as.factor(genre)


df <- data.frame(
  name = c("Ali", "Sara"),
  age = c(20, 22)
)

str(df)



scores <- c(85, 90, 78)
names(scores) <- c('Alice', 'Bob', 'Peter')
scores["Bob"]


x <- c(5, 10, 15, 20, 25)
x[3] <- -10; x 

x <- append(x, 99, 2); x
      
x <- 1L
typeof(x)

x <- c(5, 10, 15, 20, 25)
typeof(x)
class(x)
str(x)
storage.mode(x)

as.factor(x)
typeof(x)


#class () -----> for high-level category or object type
# used for mostly : data frames; factors; dates; models; user_defined_object

#typeof() -----> for internal low-level storage type. 
# mostly for interger, double, character, logical, list

## STorage.mode()  is more related to compatibility wiith language code.

## str() stand for structure and give a compact summary of type, class, dimensions, value, str of complex object 
# mostly used for dataset explorations.

#double in R mean it representing numeric by defaults but can float, point or numbers
#
m <- matrix(c(1:12),ncol=4)
m
s1 <- m[c(T,T,F),c(T,T,T,T)]
print(s1)




######################################################################
######################################################################
############# ARRAYS ###########################################
rm(list = ls())

a <- array(sample(10:50, size=12, replace = T), dim=c(2,3,2))
a


v1 <- c(1,2,3,4,5)
v2 <- c(10,11,12,13,14,15)

arr <-array(c(v1,v2), dim = c(3,3,2), dimnames = NULL)
arr


######## matrice
rand_int <- sample(1:10, size=24, replace = TRUE)
arr2 <- array(rand_int, dim=c(3,2,4))
arr2

####### assing to arr
rnames <- c('r1','r2','r3')
cnames <- c('c1','c2','c3')
mnames <- c('m1','m2')
dimnames(arr) <- list(rnames, cnames, mnames)
arr

#second row from second matrix
arr[2,,2]

# 3rd row of 3rd of matrix
arr[3,3,1] # arr['r3','c3','m1']

arr[ , , ]
# element > 5 of row 2 matrix 2
arr[2,arr[2,,2]>5,2]

######## create student data frame
Name <-c('Alice','Bob','Charlie','David','Eva')
Age <- c(20,22,21,23,20)
Grade <- c(85,92,78,89,95)
student <- data.frame(Name,Age,Grade)
student

# structure of the dataframe
str(student)
class(student)

# retrieve first 3 row of student
student[1:3,]

# calculate the mean of age
mean(student[,'Age']) # mean(student$Age) , mean(student[,2])

# add new student to the student data frame with name "Frank' 
# age = 24 and grade= 88

new_student <- data.frame(Name="frank",Age=24,Grade=88)
student  <- rbind(student,new_student)
student

# create 