from database import query


async def get_fap_list(limit: int = 10, offset: int = 0, estado: str | None = None):
    # Consulta básica con filtros opcionales
    sql = """
    SELECT id_fap, nro_fap, nrooatenc, motivo_consulta, fecha_arribo_pac, estado_fap
    FROM fap
    """
    params = []

    if estado:
        sql += " WHERE estado_fap = %s"
        params.append(estado)

    sql += " ORDER BY fecha_arribo_pac DESC LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    rows = await query(sql, tuple(params))

    result = []
    for r in rows:
        result.append(
            {
                "id_fap": r[0],
                "nro_fap": r[1],
                "nrooatenc": r[2],
                "motivo_consulta": r[3],
                "fecha_arribo_pac": r[4].strftime("%Y-%m-%d %H:%M") if r[4] else None,
                "estado_fap": r[5],
            }
        )
    return result
