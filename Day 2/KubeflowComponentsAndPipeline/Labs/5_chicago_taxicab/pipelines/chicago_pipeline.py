import kfp
from kfp import components

COMPONENT_URL = 'https://raw.githubusercontent.com/MavenCode/KubeflowTraining/master/Day%202/KubeflowComponentsAndPipeline/Labs/5_chicago_taxicab/components'

chicago_taxi_dataset_op = components.load_component_from_url(f'{COMPONENT_URL}/datasets/Chicago%20Taxi/component.yaml')
pandas_transform_csv_op = components.load_component_from_url(
    f'{COMPONENT_URL}/pandas/Transform_DataFrame/in_CSV_format/component.yaml')

catboost_train_classifier_op = components.load_component_from_url(
    f'{COMPONENT_URL}/Train_classifier/from_CSV/component.yaml')
catboost_train_regression_op = components.load_component_from_url(
    f'{COMPONENT_URL}/Train_regression/from_CSV/component.yaml')
catboost_predict_classes_op = components.load_component_from_url(
    f'{COMPONENT_URL}/Predict_classes/from_CSV/component.yaml')
catboost_predict_values_op = components.load_component_from_url(
    f'{COMPONENT_URL}/Predict_values/from_CSV/component.yaml')
catboost_predict_class_probabilities_op = components.load_component_from_url(
    f'{COMPONENT_URL}/CatBoost/Predict_class_probabilities/from_CSV/component.yaml')
catboost_to_apple_op = components.load_component_from_url(
    f'{COMPONENT_URL}/convert_CatBoostModel_to_AppleCoreMLModel/component.yaml')
catboost_to_onnx_op = components.load_component_from_url(
    f'{COMPONENT_URL}/convert_CatBoostModel_to_ONNX/component.yaml')


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

    catboost_train_regression_task = catboost_train_regression_op(
        training_data=training_data_in_csv,
        loss_function='RMSE',
        label_column=0,
        num_iterations=200,
    )

    regression_model = catboost_train_regression_task.outputs['model']

    catboost_train_classifier_task = catboost_train_classifier_op(
        training_data=training_data_for_classification_in_csv,
        label_column=0,
        num_iterations=200,
    )

    classification_model = catboost_train_classifier_task.outputs['model']

    evaluation_data_for_regression_in_csv = training_data_in_csv
    evaluation_data_for_classification_in_csv = training_data_for_classification_in_csv

    catboost_predict_values_op(
        data=evaluation_data_for_regression_in_csv,
        model=regression_model,
        label_column=0,
    )

    catboost_predict_classes_op(
        data=evaluation_data_for_classification_in_csv,
        model=classification_model,
        label_column=0,
    )

    catboost_predict_class_probabilities_op(
        data=evaluation_data_for_classification_in_csv,
        model=classification_model,
        label_column=0,
    )

    catboost_to_apple_op(regression_model)
    catboost_to_apple_op(classification_model)

    catboost_to_onnx_op(regression_model)
    catboost_to_onnx_op(classification_model)


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(chicago_taxi_pipeline, "chicago_pipeline-2.zip")
    client = kfp.Client(host='pipelines-api.kubeflow.svc.cluster.local:8888')
    # client.list_pipelines()
    pipeline_info = client.upload_pipeline('chicago_pipeline-2.zip', pipeline_name='chicago_pipeline-2')

    # my_experiment = client.create_experiment(name='chicago_pipeline-2-experiments')
    # my_run = client.run_pipeline(my_experiment.id, 'my-chicago-taxi-run', 'chicago_pipeline-2.zip')
