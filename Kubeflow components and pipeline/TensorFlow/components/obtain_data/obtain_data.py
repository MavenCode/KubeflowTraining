def obtain_data():
    #importing libraries
    import joblib
    import pandas as pd
    #importing the data
    data = pd.read_csv("https://raw.githubusercontent.com/MavenCode/KubeflowTraining/master/Data/Churn_Modelling.csv")

    #serialize data to be used
    joblib.dump(data, 'data')

if __name__ == '__main__':
    obtain_data()
