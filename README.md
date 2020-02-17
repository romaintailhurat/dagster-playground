# Assessing Dagster

[Dagster](https://github.com/dagster-io/dagster) is a data pipeline tool.

Running a pipeline via Python:

```bash
python3 cereal.py
```

Running dagit (dagster UI):

```bash
dagit -f cereal.py -n cereal_pipeline
```

Executing test (ensure pytest is installed):

```bash
pytest test_cereal.py
```