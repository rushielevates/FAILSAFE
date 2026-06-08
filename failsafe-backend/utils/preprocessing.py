def preprocess_new_data(raw_df, pipeline):
    """
    Use the pipeline's built-in preprocessing.
    The pipeline already has LabelEncoders fitted on training data.
    """
    return pipeline.preprocess(raw_df)