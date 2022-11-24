from sqlalchemy import create_engine
import pymysql
import mysql.connector
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
# DEFINE THE DATABASE CREDENTIALS
user = 'bita'
password = 'pishraft123'
host = '127.0.0.1'
port = 3306
database = 'cardatabase1'


# PYTHON FUNCTION TO CONNECT TO THE MYSQL DATABASE AND
# RETURN THE SQLACHEMY ENGINE OBJECT
def get_connection():
    return create_engine(url="mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database))

try:

    # GET THE CONNECTION OBJECT (ENGINE) FOR THE DATABASE
        engine = get_connection()
        print(
        f"Connection to the {host} for user {user} created successfully.")
except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)
########################################
#run sql
#Honda Accord
sql_query = pd.read_sql_query('''SELECT * FROM honda_table where model_names = 'Honda Accord' ''',engine)
df = pd.DataFrame(sql_query, columns = ['years', 'miles', 'prices'])
#print(df)
print(type(df))
########################################
##ml_model
print(df)
print('___________________________________________________________________')
data=df.values
print(data)
print(type(data))
print(type((data[0,:])))
X=data[1:,0:2]
Y=data[1:,2]
print(np.shape(Y))
print(Y)
print('_____________________')
for i in range(len(Y)) :
    Y[i]=Y[i].replace(',','.')
Y=[float(a) for a in Y]

for i in range(len(X)):
    for j in range(len(X[i])):
        # print(X[i][j])
        X[i][j]=float(X[i][j].replace(',','.'))


print(np.shape(X))
print(np.shape(Y))
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
# x_train , x_test , y_train , y_test =train_test_split(data)
# print(np.shape(x_train))

print(np.shape(X_train))
print(np.shape(X_test))
print(np.shape(Y_train))
print(np.shape(Y_test))
##########################################################################
#develping model
model=LinearRegression()
print(type(Y_train[0]))
model.fit(X_train,Y_train)
# print(metrics.roc_auc_score(Y_train,LogisticRegression.predict_proba(X_train)))
y_pred=model.predict(X_test)

mae = mean_absolute_error(Y_test, y_pred)
mse = mean_squared_error(Y_test, y_pred)
rmse = np.sqrt(mse)
print(f'Mean absolute error: {mae:.2f}')
print(f'Mean squared error: {mse:.2f}')
print(f'Root mean squared error: {rmse:.2f}')
