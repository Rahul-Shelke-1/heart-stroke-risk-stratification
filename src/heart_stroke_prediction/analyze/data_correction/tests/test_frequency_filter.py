
from heart_stroke_prediction.data_correction.schema_correction import (
    ColumnNameCorrector, FrequencyFilter, ValueCorrector)

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

my_dict = {
        "id": "id",
        "gender": "gender",
        "age": "age",
        "hypertension": "hypertension",
        "heart_disease": "heart_disease",
        "ever_married": "ever_married",
        "work_type": "work_type",
        "Residence_type": "residence_type",
        "avg_glucose_level": "avg_glucose_level",
        "bmi": "bmi",
        "smoking_status": "smoking_status",
        "stroke": "stroke"
    }

def test_ferquency_filter(raw_dataframe):
    # correct the column names
    name_correct = ColumnNameCorrector(my_dict)
    df = name_correct.transform(raw_dataframe)

    # value correction
    value_correction_dict = {
        'gender': {
            'Male': 'male',
            'Female': 'female',
            'Other': 'other'
        },
    }

    value_correct = ValueCorrector(value_correction_dict)
    df = value_correct.transform(df)

    # frquency filter
    frequency_filter = FrequencyFilter(threshold=1, action="drop")
    df = frequency_filter.fit_transform(df)

    assert df['gender'].nunique() == 2
