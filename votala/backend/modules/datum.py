to_schemas = lambda schema_class, datum: [  # using tuples for being statically alocated memory and faster than lists.
    *map(lambda data: schema_class.from_orm(data), datum)
]
