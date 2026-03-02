"""
Script 03 — Verificar conexión BigQuery y documentar tablas GDELT disponibles
Prerequisito: gcloud auth application-default login (correr en terminal)
"""

from google.cloud import bigquery

PROJECT = "gdelt-bq"

def test_connection(client: bigquery.Client) -> None:
    """Hace una query trivial para confirmar acceso."""
    query = "SELECT 1 AS test"
    result = client.query(query).result()
    for row in result:
        print(f"  Conexión OK: {row['test']}")


def explore_tables(client: bigquery.Client) -> None:
    """Lista datasets y tablas disponibles en gdelt-bq."""
    datasets = list(client.list_datasets())
    print(f"\nDatasets en {PROJECT}:")
    for ds in datasets:
        print(f"  {ds.dataset_id}")
        tables = list(client.list_tables(ds.dataset_id))
        for t in tables:
            print(f"    └── {t.table_id}")


def sample_gkg_schema(client: bigquery.Client) -> None:
    """Muestra schema de gkg_partitioned y un ejemplo."""
    table = client.get_table(f"{PROJECT}.gdeltv2.gkg_partitioned")
    print(f"\nSchema de gkg_partitioned ({len(table.schema)} campos):")
    for field in table.schema:
        print(f"  {field.name:30s} {field.field_type}")

    print("\nEjemplo reciente (1 fila):")
    q = f"""
    SELECT DATE, SourceCommonName, DocumentIdentifier,
           V2Tone, V2Organizations, V2Themes, V2Locations
    FROM `{PROJECT}.gdeltv2.gkg_partitioned`
    WHERE DATE > 20260101
    LIMIT 1
    """
    row = next(client.query(q).result())
    for k, v in dict(row).items():
        val = str(v)[:120] if v else "NULL"
        print(f"  {k}: {val}")


def estimate_china_coverage(client: bigquery.Client) -> None:
    """Estima cuántos artículos/eventos de China hay por año en GKG."""
    print("\nVolumen de artículos con China en GKG (dry run para estimar costo):")
    q = f"""
    SELECT DIV(DATE, 10000) AS year, COUNT(*) AS n_articles
    FROM `{PROJECT}.gdeltv2.gkg_partitioned`
    WHERE DATE BETWEEN 20170101 AND 20241231
    AND UPPER(V2Organizations) LIKE '%CHIN%'
    GROUP BY year
    ORDER BY year
    """
    job_config = bigquery.QueryJobConfig(dry_run=True)
    job = client.query(q, job_config=job_config)
    bytes_gb = job.total_bytes_processed / 1e9
    print(f"  Bytes estimados a procesar: {bytes_gb:.1f} GB")
    print(f"  Costo estimado (tier gratuito 1TB/mes): {'GRATIS' if bytes_gb < 1000 else f'~${bytes_gb/1000 * 6:.2f} USD'}")


if __name__ == "__main__":
    print("=== Verificando conexión BigQuery ===")
    client = bigquery.Client()
    print(f"  Proyecto activo: {client.project}")

    test_connection(client)
    explore_tables(client)
    sample_gkg_schema(client)
    estimate_china_coverage(client)
