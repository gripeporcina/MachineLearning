from sklearn import tree	
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

X = [[181,80,44],[177,70,43],[160,60,38],[154,54,37],
	 [166,65,40],[190,90,47],[175,64,39],[177,70,40],[159,55,37],
	 [171,75,42],[181,85,43]]

Y =['male','female','female','female','male','male',
	'male','female','male','female','male']

#Classifiers, Using the default values
clf = tree.DecisionTreeClassifier()
clf_2 = KNeighborsClassifier()
clf_3 = LinearDiscriminantAnalysis()

#Training th models
clf = clf.fit(X,Y)
clf_2 = clf_2.fit(X,Y)
clf_3 = clf_3.fit(X,Y)

#Test
prediction = clf.predict([[190,70,43]])
prediction_2 = clf_2.predict([[190,70,43]])
prediction_3 = clf_3.predict([[190,70,43]])

print (prediction)
print (prediction_2)
print (prediction_3)	 
