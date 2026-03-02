# Setup GCP — Estado actual

## Cuenta configurada ✅

- **Cuenta:** salareuniones113@gmail.com
- **Proyecto:** tomasdata-gdelt-research
- **Créditos:** $300 disponibles (cuenta nueva)
- **Separado de:** Orsan (tomas@orsan.ai)

## Para retomar en una sesión nueva

Si las credenciales expiran o cambias de máquina:

```bash
gcloud config set account salareuniones113@gmail.com
gcloud config set project tomasdata-gdelt-research
gcloud auth application-default login --account=salareuniones113@gmail.com
gcloud auth application-default set-quota-project tomasdata-gdelt-research

# Verificar
source gdelt_env/bin/activate
python notebooks/03_bigquery_conexion.py
```

## Próximo paso inmediato

```bash
source gdelt_env/bin/activate
python notebooks/07_gkg_discovery.py
```

Costo estimado: ~$10-12 (cubierto por créditos). Pide confirmación antes de ejecutar.

## Historial de proyectos GCP usados

| Proyecto | Cuenta | Estado | Notas |
|----------|--------|--------|-------|
| tomas-gdelt-china-2024 | tomas@orsan.ai | Abandonado | Dentro de org Orsan, no usar |
| tomasdata-gdelt-research | salareuniones113@gmail.com | **Activo** | $300 créditos disponibles |
