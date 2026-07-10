
from heart_stroke_prediction.data_correction.schema_correction import \
    ValueCorrector

value_correction_dict = {
    'gender': {'Male': 'male', 'Female': 'female', 'Other': 'other'},
    'ever_married': {'Yes':'yes', 'No': 'no'},
    'residence_type': {'Urban': 'urban', 'Rural': 'rural'},
    'smoking_status': {'formerly smoked': 'formerly_smoked',
                            'never smoked': 'never_smoked',
                            'Unknown': 'unknown'},
    'work_type': {'Private':'private', 'self-employed': 'self_employed',
                            'Govt_job': 'govt_job', 'Never_worked': 'never_worked',
                            'children': 'children'},
}

def test_value_correction_with_dictionary(raw_dataframe):
    value_correction_dict = {
        'gender': {
            'Male': 'male',
            'Female': 'female',
            'Other': 'other'
        },
    }

    value_correct = ValueCorrector(value_correction_dict)
    df = value_correct.transform(raw_dataframe)

    expected_output = value_correction_dict['gender'].values()
    unique_vals = df['gender'].unique()

    assert list(unique_vals) == list(expected_output)
