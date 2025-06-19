import yamale

def validate_profile(profile_path, schema_path="ironshell/profile_schema.yaml"):
    schema = yamale.make_schema(schema_path)
    data = yamale.make_data(profile_path)
    yamale.validate(schema, data)