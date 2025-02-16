def sql_query(
        model,
        modelSerializer,
        column,table,
        where,
        parametars
        ):
    query = model.objects.raw(f"SELECT {column} FROM {table} WHERE {where} ",parametars)
    return modelSerializer(query, many=True).data