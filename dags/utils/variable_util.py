from airflow.models import Variable


def get_variable(variable_name):
    """
    To get variable in Airflow MWAA or local machine
    If it's a local variable, it should be start with `AIRFLOW_VAR_` prefix.
    See https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#mocking-variables-and-connections
    """
    return Variable.get(variable_name, default_var=None)
