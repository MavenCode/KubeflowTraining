import kfp
from kfp import components

COMPONENT_URI = 'https://raw.githubusercontent.com/MavenCode/KubeflowTraining/master/Day%202/KubeflowComponentsAndPipeline/Labs/5_chicago_taxi_cab/components'

chicago_taxi_dataset_op = components.load_component_from_url(f'{COMPONENT_URI}/chicago_taxi_trips/component.yaml')
pandas_transform_csv_op = components.load_component_from_url(f'{COMPONENT_URI}/pandas_transform_df/component.yaml')

train_classifier_op = components.load_component_from_url(f'{COMPONENT_URI}/train_classifier/component.yaml')
train_regression_op = components.load_component_from_url(f'{COMPONENT_URI}/train_regression/component.yaml')
predict_classes_op = components.load_component_from_url(f'{COMPONENT_URI}/predict_classes/component.yaml')
predict_values_op = components.load_component_from_url(f'{COMPONENT_URI}/predict_values/component.yaml')

predict_class_probabilities_op = components.load_component_from_url(
    f'{COMPONENT_URI}/predict_class_probabilities/component.yaml')
export_model_to_AppleCoreML_op = components.load_component_from_url(
    f'{COMPONENT_URI}/export_model_to_AppleCoreML/component.yaml')
export_model_to_ONNX_op = components.load_component_from_url(f'{COMPONENT_URI}/export_model_to_ONNX/component.yaml')


def chicago_taxi_pipeline():
    training_data_in_csv = chicago_taxi_dataset_op(
        where='trip_start_timestamp >= "2019-01-01" AND trip_start_timestamp < "2019-02-01"',
        select='tips,trip_seconds,trip_miles,pickup_community_area,dropoff_community_area,fare,tolls,extras,trip_total',
        limit=10000,
    ).output

    training_data_for_classification_in_csv = pandas_transform_csv_op(
        table=training_data_in_csv,
        transform_code='''df.insert(0, "was_tipped", df["tips"] > 0); del df["tips"]''',
    ).output

    evaluation_data_for_regression_in_csv = training_data_in_csv
    evaluation_data_for_classification_in_csv = training_data_for_classification_in_csv

    train_regression_task = train_regression_op(
        training_data="training_data_in_csv",
        loss_function='RMSE',
        label_column=0,
        num_iterations=200,
    )

    regression_model = train_regression_task.outputs['model']



if __name__ == '__main__':
    kfp.compiler.Compiler().compile(chicago_taxi_pipeline, __file__ + '02222020.zip')