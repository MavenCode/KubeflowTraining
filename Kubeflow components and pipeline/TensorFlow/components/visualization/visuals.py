#importing libraries
import argparse
from typing import NamedTuple

def visuals(test_loss,test_acc,matrix_data) -> NamedTuple('output', [('mlpipeline_ui_metadata', 'UI_metadata'), 
                                                           ('mlpipeline_metrics', 'Metrics')]):
    #importing libraries
    import joblib
    import numpy as np
    import pandas as pd
    import json

    #loading the metrics
    test_loss =joblib.load(test_loss)
    test_acc = joblib.load(test_acc)
    matrix_data = joblib.load(matrix_data)
    vocab = [0,1]

    metadata = {
        'outputs' : [{
          'type': 'confusion_matrix',
          'format': 'csv',
          'schema':[
              {'name': 'target', 'type': 'CATEGORY'},
              {'name': 'predicted', 'type': 'CATEGORY'},
              {'name': 'count', 'type': 'NUMBER'},
          ],
          'source': matrix_data.to_csv(header=False, index=False),
          'storage':'inline',
          'labels': list(map(str,vocab)),
        }]
      }

    metrics = {
    'metrics': [{
        'name': 'Accuracy',
        'numberValue':  float(test_acc),
        'format': "PERCENTAGE",
    }, {
        'name': 'Loss',
        'numberValue':  float(test_loss),
        'format': "PERCENTAGE",
    }]}
    
    from collections import namedtuple
    output = namedtuple('output', ['mlpipeline_ui_metadata', 'mlpipeline_metrics'])
    visual = output(json.dumps(metadata), json.dumps(metrics))
    with open('mlpipeline-ui-metadata.json', 'w') as met:
        met.write(visual.mlpipeline_ui_metadata)
    with open('mlpipeline-metrics.json', 'w') as mat:
        mat.write(visual.mlpipeline_metrics)

#defining and parsing arguments
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--test_loss')
    parser.add_argument('--test_acc')
    parser.add_argument('--matrix_data')
    args = parser.parse_args()
    visuals(args.test_loss, args.test_acc, args.matrix_data)

"""
 #saving pred and actual as csv file
    vocab = [0,1]
    cm = confusion_matrix(y_test, y_pred, labels=vocab)
    cm_data = []
    for target_index,target_row in enumerate(cm):
        for predicted_index, count in enumerate(target_row):
            cm_data.append((vocab[target_index], vocab[predicted_index], count))

    cm_df = pd.DataFrame(cm_data, columns=['target','predicted','count'])
    
    #serialize data to be used for confusion matrix
    joblib.dump(cm_df, 'matrix_data')
"""