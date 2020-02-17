import csv
from dagster import execute_pipeline, execute_solid, pipeline, solid

@solid
def load_cereals(context):
    dataset_path = "data/cereal.csv"
    with open(dataset_path) as fd:
        cereals = [row for row in csv.DictReader(fd)]
    context.log.info(f"There is {len(cereals)} cereals in the dataset {dataset_path}")
    return cereals

@solid
def sort_by_calories(context, cereals):
    sorted_cereals = list(
        sorted(cereals, key = lambda cereal: cereal["calories"])
        )
    context.log.info(
        'Least caloric cereal: {least_caloric}'.format(
            least_caloric=sorted_cereals[0]['name']
        )
    )
    context.log.info(
        'Most caloric cereal: {most_caloric}'.format(
            most_caloric=sorted_cereals[-1]['name']
        )
    )

@pipeline
def cereal_pipeline():
    sort_by_calories(load_cereals())

if __name__ == "__main__":
    result = execute_pipeline(cereal_pipeline)
    assert result.success