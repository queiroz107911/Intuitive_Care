from typing import Optional, List, Dict, Any

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from .database import get_db

app = FastAPI(title="Intuitive Care API", version="1.0.0")

# libera acesso do frontend (Vue) se você usar depois
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção, restrinja
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def normalize_cnpj(cnpj: str) -> str:
    return "".join(ch for ch in cnpj if ch.isdigit())

def clamp_pagination(page: int, limit: int):
    if page < 1:
        page = 1
    if limit < 1:
        limit = 10
    if limit > 200:
        limit = 200
    offset = (page - 1) * limit
    return page, limit, offset

def table_exists(db: Session, table_name: str) -> bool:
    q = text(
        """
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = DATABASE()
          AND table_name = :table_name
        """
    )
    return int(db.execute(q, {"table_name": table_name}).scalar() or 0) > 0


@app.get("/api/operadoras")
def listar_operadoras(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=200),
    db: Session = Depends(get_db),
):
    page, limit, offset = clamp_pagination(page, limit)

    has_operadoras = table_exists(db, "operadoras")

    if has_operadoras:
        total = db.execute(text("SELECT COUNT(*) FROM operadoras")).scalar() or 0
        rows = db.execute(
            text(
                """
                SELECT CNPJ, Razao_Social, Modalidade, UF, REG_ANS
                FROM operadoras
                ORDER BY Razao_Social
                LIMIT :limit OFFSET :offset
                """
            ),
            {"limit": limit, "offset": offset},
        ).mappings().all()
    else:
        if not table_exists(db, "despesas_consolidadas"):
            raise HTTPException(
                status_code=500,
                detail="Crie a tabela 'operadoras' ou 'despesas_consolidadas' no banco.",
            )

        total = db.execute(
            text(
                """
                SELECT COUNT(*) FROM (
                    SELECT DISTINCT CNPJ
                    FROM despesas_consolidadas
                ) t
                """
            )
        ).scalar() or 0

        rows = db.execute(
            text(
                """
                SELECT
                    CNPJ,
                    MAX(Razao_Social) AS Razao_Social,
                    MAX(Modalidade) AS Modalidade,
                    MAX(UF) AS UF,
                    MAX(REG_ANS) AS REG_ANS
                FROM despesas_consolidadas
                GROUP BY CNPJ
                ORDER BY Razao_Social
                LIMIT :limit OFFSET :offset
                """
            ),
            {"limit": limit, "offset": offset},
        ).mappings().all()

    return {
        "page": page,
        "limit": limit,
        "total": int(total),
        "items": [dict(r) for r in rows],
    }


@app.get("/api/operadoras/{cnpj}")
def detalhe_operadora(cnpj: str, db: Session = Depends(get_db)):
    cnpj = normalize_cnpj(cnpj)

    has_operadoras = table_exists(db, "operadoras")

    if has_operadoras:
        row = db.execute(
            text(
                """
                SELECT CNPJ, Razao_Social, Modalidade, UF, REG_ANS
                FROM operadoras
                WHERE CNPJ = :cnpj
                LIMIT 1
                """
            ),
            {"cnpj": cnpj},
        ).mappings().first()
    else:
        if not table_exists(db, "despesas_consolidadas"):
            raise HTTPException(status_code=500, detail="Tabela 'despesas_consolidadas' não existe.")

        row = db.execute(
            text(
                """
                SELECT
                    CNPJ,
                    MAX(Razao_Social) AS Razao_Social,
                    MAX(Modalidade) AS Modalidade,
                    MAX(UF) AS UF,
                    MAX(REG_ANS) AS REG_ANS
                FROM despesas_consolidadas
                WHERE CNPJ = :cnpj
                GROUP BY CNPJ
                LIMIT 1
                """
            ),
            {"cnpj": cnpj},
        ).mappings().first()

    if not row:
        raise HTTPException(status_code=404, detail="Operadora não encontrada.")

    return dict(row)


@app.get("/api/operadoras/{cnpj}/despesas")
def historico_despesas_operadora(
    cnpj: str,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    ano: Optional[int] = Query(None),
    trimestre: Optional[int] = Query(None, ge=1, le=4),
    db: Session = Depends(get_db),
):
    cnpj = normalize_cnpj(cnpj)
    page, limit, offset = clamp_pagination(page, limit)

    if not table_exists(db, "despesas_consolidadas"):
        raise HTTPException(status_code=500, detail="Tabela 'despesas_consolidadas' não existe.")

    filters = ["CNPJ = :cnpj"]
    params: Dict[str, Any] = {"cnpj": cnpj, "limit": limit, "offset": offset}

    if ano is not None:
        filters.append("Ano = :ano")
        params["ano"] = ano

    if trimestre is not None:
        filters.append("Trimestre = :trimestre")
        params["trimestre"] = trimestre

    where_clause = " AND ".join(filters)

    total = db.execute(
        text(
            f"""
            SELECT COUNT(*) FROM (
                SELECT Ano, Trimestre
                FROM despesas_consolidadas
                WHERE {where_clause}
                GROUP BY Ano, Trimestre
            ) t
            """
        ),
        params,
    ).scalar() or 0

    rows = db.execute(
        text(
            f"""
            SELECT
                Ano,
                Trimestre,
                SUM(ValorDespesas) AS ValorDespesas
            FROM despesas_consolidadas
            WHERE {where_clause}
            GROUP BY Ano, Trimestre
            ORDER BY Ano, Trimestre
            LIMIT :limit OFFSET :offset
            """
        ),
        params,
    ).mappings().all()

    return {
        "page": page,
        "limit": limit,
        "total": int(total),
        "cnpj": cnpj,
        "items": [dict(r) for r in rows],
    }