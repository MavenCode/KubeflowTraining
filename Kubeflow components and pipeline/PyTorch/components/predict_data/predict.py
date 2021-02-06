#importing libraries
import argparse

def predict(X_test, y_test,model):
    #importing libraries
    import numpy as np
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import Dataset, DataLoader

    #loading the model and inputs
    X_test = np.load(X_test)
    y_test = np.load(y_test)

     #defining neural network architecture
    class binaryClassification(nn.Module):
        def __init__(self):
            super(binaryClassification, self).__init__()
            #number of input features is 12
            self.layer_1 = nn.Linear(12, 16)
            self.layer_2 = nn.Linear(16, 8)
            self.layer_out = nn.Linear(8, 1) 
            self.relu = nn.ReLU()
            self.dropout = nn.Dropout(p=0.1)
            self.batchnorm1 = nn.BatchNorm1d(16)
            self.batchnorm2 = nn.BatchNorm1d(8)       
        #feed forward network
        def forward(self, inputs):
            x = self.relu(self.layer_1(inputs))
            x = self.batchnorm1(x)
            x = self.relu(self.layer_2(x))
            x = self.batchnorm2(x)
            x = self.dropout(x)
            x = self.layer_out(x)
            return x
    
    #loading model
    classifier = binaryClassification()
    classifier.load_state_dict(torch.load(model))
    
     #test data
    class testData(Dataset):
        def __init__(self, X_data):
            self.X_data = X_data

        def __getitem__(self,index):
            return self.X_data[index]

        def __len__(self):
            return len(self.X_data)

    test_data = testData(torch.FloatTensor(X_test))
    test_loader = DataLoader(dataset=test_data, batch_size=1, num_workers=0)
    #function to calculate accuracy
    def binary_acc(y_pred, y_test):
        y_pred_tag = torch.round(torch.sigmoid(y_pred))
        results_sum = (y_pred_tag == y_test).sum().float()
        acc = results_sum/y_test.shape[0]
        acc =torch.round(acc*100)
        return acc

    #test model
    y_pred_list = []
    classifier.eval()
    #ensures no back propagation during testing and reduces memeory usage
    with torch.no_grad():
        for X_batch in test_loader:
            y_test_pred = classifier(X_batch)
            y_test_pred = torch.sigmoid(y_test_pred)
            y_pred_tag = torch.round(y_test_pred)
            y_pred_list.append(y_pred_tag.cpu().numpy())
        y_pred_list = [i.squeeze().tolist() for i in y_pred_list] 

    acc = binary_acc(torch.FloatTensor(y_pred_list), torch.FloatTensor(y_test))
    accu = acc.item()
    accuracy = accu/len(y_pred_list)

    with open('results.txt', 'w') as result:
        result.write(" Prediction: {}, Actual: {}, Acc: {}".format(y_pred_list,y_test,accuracy))
    
    print('Prediction has be saved successfully!')

#defining and parsing arguments
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--X_test')
    parser.add_argument('--y_test')
    parser.add_argument('--model')
    args = parser.parse_args()
    print('Prediction has be saved successfully!')
    predict(args.X_test, args.y_test, args.model)
    