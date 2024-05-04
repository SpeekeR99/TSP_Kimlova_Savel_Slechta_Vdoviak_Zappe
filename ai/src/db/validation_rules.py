# sample

validation_rules = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "age"],
            "properties": {
                "name": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "age": {
                    "bsonType": "int",
                    "minimum": 0,
                    "description": "must be an integer and is required"
                }
            }
        }
    }
}