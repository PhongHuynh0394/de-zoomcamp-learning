import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def camel_to_snake(col):
    if col[0].isupper():
        is_upper = True
    else: is_upper = False

    result = []
    # Aa
    for char in col:
        # aA -> a + _A
        if char.isupper() and not is_upper:
            result.extend(["_", char.lower()])
            is_upper = True
        # Aa -> a+_ +a
        elif char.islower() and is_upper:
            last_char = result.pop()
            result.extend(["_" ,last_char ,char.lower()])
            is_upper = False
        else:
            result.append(char.lower())

    if result[0] == '_':
        result = result[1:]

    return "".join(result)

@transformer
def transform(df, *args, **kwargs):
    # Remove rows where the passenger count is equal to 0 or the trip distance is equal to zero.
    df = df[(df['passenger_count'] != 0) & (df['trip_distance'] != 0)]
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    # Create a new column lpep_pickup_date by converting lpep_pickup_datetime to a date.
    df['lpep_pickup_date'] = df['lpep_pickup_datetime'].dt.date
    # Rename columns in Camel Case to Snake Case
    df.columns = [camel_to_snake(col) for col in df.columns]
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

@test
def test_passenger(output, *arg) -> None:
    assert len(output[output['passenger_count'] == 0]) == 0, 'Passenger = 0'

@test
def test_distance(output, *arg) -> None:
    assert len(output[output['trip_distance'] == 0]) == 0, "Distance = 0"
