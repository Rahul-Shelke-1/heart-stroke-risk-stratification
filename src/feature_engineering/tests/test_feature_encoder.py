import pytest

from src.feature_engineering.feature_encoder import (CustomeOnehotEncoder,
                                                     CustomeOrdinalEncoder)


@pytest.mark.parametrize("column_name, custom_mapping, expected_output", [
    ('gender', {'gender': {'Male': 0, 'Female': 1, 'Other': 2} }, ['Male', 'Female', 'Other']),
    ]
)
def test_custom_oridnal_encoder(raw_dataframe, column_name, custom_mapping, expected_output):

    encoder = CustomeOrdinalEncoder(
        columns=[column_name],
        custom_mapping= custom_mapping,
        return_array=False
        )

    df_ = encoder.fit_transform(raw_dataframe)

    output = encoder.inverse_transform(df_)[column_name].unique()

    assert expected_output == list(output)

@pytest.mark.parametrize("column_names, keep_columns, expected_output", [
    (['gender'], ['gender__Male', 'gender__Female', 'gender__Other'], ['Male', 'Female', 'Other']),
    ]
)
def test_custom_onehot_encoder(raw_dataframe, column_names, keep_columns, expected_output):

    encoder = CustomeOnehotEncoder(
        columns=column_names,
        keep_columns=keep_columns
    )

    df_ = encoder.fit_transform(raw_dataframe[column_names])

    output = encoder.inverse_transform(df_).columns().to_list()

    assert expected_output == output
