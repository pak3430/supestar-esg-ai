FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SUPESTAR_HOST=0.0.0.0 \
    SUPESTAR_PORT=8080 \
    SUPESTAR_AI_PROVIDER=disabled

WORKDIR /app

COPY 05_identity_pipeline/06_atomic_skills/ ./05_identity_pipeline/06_atomic_skills/
COPY 05_identity_pipeline/07_run_skills/ ./05_identity_pipeline/07_run_skills/
COPY ccs_authoring/supestar_mvp_v3/ ./ccs_authoring/supestar_mvp_v3/
COPY ccs_composite_authoring/ ./ccs_composite_authoring/
COPY 06_runtime/src/supestar_web/ ./06_runtime/src/supestar_web/

RUN mkdir -p /app/06_runtime/runs/supestar_web_v1 \
    && useradd --create-home --uid 10001 supestar \
    && chown -R supestar:supestar /app/06_runtime/runs

USER supestar
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python3 -c "import json,urllib.request; assert json.load(urllib.request.urlopen('http://127.0.0.1:8080/api/health'))['status']=='ok'"

CMD ["python3", "06_runtime/src/supestar_web/server.py"]
