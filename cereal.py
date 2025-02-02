import csv
from dagster import execute_pipeline, execute_solid, pipeline, solid

@solid
def load_cereals(context):
    dataset_path = "data/cereal.csv"
    with open(dataset_path) as fd:
        cereals = [row for row in csv.DictReader(fd)]
    return cereals

@solid
def sort_by_calories(context, cereals):
    sorted_cereals = list(
        sorted(cereals, key = lambda cereal: int(cereal["calories"]))
        )
    least_caloric = sorted_cereals[0]["name"]
    most_caloric = sorted_cereals[-1]["name"]
    return(least_caloric, most_caloric)

@solid
def sort_by_proteins(context, cereals):
    sorted_cereals = list(
        sorted(cereals, key = lambda cereal: int(cereal["protein"]))
        )
    least_protein = sorted_cereals[0]["name"]
    most_protein = sorted_cereals[-1]["name"]
    return(least_protein, most_protein)

@solid
def display_results(context, calorie_results, protein_results):
    context.log.info(
        'Least caloric cereal: {least_caloric}'.format(
            least_caloric=calorie_results[0]
        )
    )
    context.log.info(
        'Most caloric cereal: {most_caloric}'.format(
            most_caloric=calorie_results[-1]
        )
    )
    context.log.info(
        'Least protein-rich cereal: {least_protein}'.format(
            least_protein=protein_results[0]
        )
    )
    context.log.info(
        'Most protein-rich cereal: {most_protein}'.format(
            most_protein=protein_results[-1]
        )
    )

@pipeline
def cereal_pipeline():
    cereals = load_cereals()
    display_results(
        calorie_results = sort_by_calories(cereals),
        protein_results = sort_by_proteins(cereals)
    )

if __name__ == "__main__":
    result = execute_pipeline(cereal_pipeline)
    assert result.success