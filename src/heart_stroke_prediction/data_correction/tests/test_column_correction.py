
from heart_stroke_prediction.data_correction.schema_correction import \
    ColumnNameCorrector

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

def test_column_correction_with_dictionary(raw_dataframe):
    name_correct = ColumnNameCorrector(my_dict)
    df = name_correct.transform(raw_dataframe)

    assert list(df.columns) == list(my_dict.values())

def test_column_correction_without_dictionary(raw_dataframe):

    name_correct = ColumnNameCorrector({})
    df = name_correct.transform(raw_dataframe)

    assert list(df.columns) == list(my_dict.values())
