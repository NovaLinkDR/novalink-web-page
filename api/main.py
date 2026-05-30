"""
NovaLink Assistant API
Backend para el chatbot de la landing page.
Sectorización por industria y captura de leads.
"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="NovaLink Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Data ──────────────────────────────────────────────────────────────

LEADS_FILE = Path(os.environ.get("LEADS_FILE", "/data/leads.json"))

INDUSTRIES = [
    "🏪 Retail / E-commerce",
    "🏥 Salud",
    "🚚 Logística y Transporte",
    "🏦 Finanzas y Contabilidad",
    "🏭 Manufactura",
    "🏗️ Construcción",
    "🎓 Educación",
    "🏛️ Gobierno / Sector Público",
    "💻 Tecnología / SaaS",
    "📞 Call Center / BPO",
    "🏨 Hotelería / Turismo",
    "🥗 Alimentos y Bebidas",
    "⚡ Energía / Utilities",
    "🚜 Agroindustria",
]

PROCESSES = [
    "🧾 Facturación y cobros",
    "📦 Inventario y stock",
    "💬 Atención al cliente",
    "📊 Reportes y análisis",
    "📋 Procesos administrativos",
    "🔍 Control de calidad",
    "🔄 Integración de sistemas",
    "📧 Gestión documental / emails",
    "👥 RRHH / onboarding",
    "📈 Marketing y ventas",
    "🚛 Logística y despachos",
    "🔐 Cumplimiento normativo",
]

COMPANY_SIZES = [
    "1-10 empleados",
    "11-50 empleados",
    "51-200 empleados",
    "201-500 empleados",
    "500+ empleados",
]

# ── Session store (in-memory) ────────────────────────────────────────

sessions: dict[str, dict] = {}


def load_leads() -> list[dict]:
    if LEADS_FILE.exists():
        return json.loads(LEADS_FILE.read_text())
    return []


def save_lead(lead: dict):
    leads = load_leads()
    leads.append(lead)
    LEADS_FILE.parent.mkdir(parents=True, exist_ok=True)
    LEADS_FILE.write_text(json.dumps(leads, indent=2, ensure_ascii=False))


# ── LLM Integration ──────────────────────────────────────────────────
# Config via environment variables:
#   LLM_API_KEY  - API key for the LLM provider
#   LLM_MODEL    - Model name (default: deepseek-chat)
#   LLM_BASE_URL - API base URL (default: https://api.deepseek.com/v1)

import httpx

LLM_API_KEY = os.environ.get("LLM_API_KEY", "")
LLM_MODEL = os.environ.get("LLM_MODEL", "deepseek-chat")
LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "https://api.deepseek.com/v1")


async def call_llm(system_prompt: str, user_message: str) -> str:
    """
    Calls the configured LLM API. Falls back to empty string (template response)
    if no API key is configured or the call fails.
    """
    if not LLM_API_KEY:
        return ""  # No LLM configured → use template fallback

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{LLM_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {LLM_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": LLM_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message},
                    ],
                    "max_tokens": 500,
                    "temperature": 0.7,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"LLM call failed: {e}")
        return ""  # Fallback to template


# ── API Models ───────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    step: int = 0
    industry: str | None = None
    processes: list[str] | None = None
    company_size: str | None = None
    email: str | None = None


class ChatResponse(BaseModel):
    session_id: str
    bot_message: str
    suggestions: list[str]
    step: int


# ── Routes ───────────────────────────────────────────────────────────

@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    sid = req.session_id or str(uuid.uuid4())[:8]

    if sid not in sessions:
        sessions[sid] = {"step": 0, "data": {}}

    session = sessions[sid]
    msg = req.message.strip()
    lower = msg.lower()

    # ── STEP 0: Bienvenida y sectorización ──────────────────────────
    if session["step"] == 0:
        session["step"] = 1
        return ChatResponse(
            session_id=sid,
            bot_message=(
                "👋 ¡Hola! Soy el asistente virtual de **NovaLink**. "
                "Estoy aquí para mostrarte cómo la automatización puede transformar tu empresa.\n\n"
                "Para empezar, ¿a qué **industria** pertenece tu negocio?"
            ),
            suggestions=INDUSTRIES,
            step=1,
        )

    # ── STEP 1: Recibir industria → preguntar procesos ──────────────
    elif session["step"] == 1:
        # Buscar si el mensaje coincide con una industria de la lista
        matched = None
        for ind in INDUSTRIES:
            ind_clean = ind.split(" ", 1)[1] if " " in ind else ind
            if ind_clean.lower() in lower or lower in ind_clean.lower():
                matched = ind
                break
        if not matched:
            matched = msg  # usar lo que escribió

        session["data"]["industry"] = matched
        session["step"] = 2
        return ChatResponse(
            session_id=sid,
            bot_message=(
                f"¡Excelente! **{matched}** es un sector con mucho potencial de automatización.\n\n"
                "Ahora dime, ¿qué **procesos u operaciones** te gustaría optimizar? "
                "Puedes seleccionar varios."
            ),
            suggestions=PROCESSES,
            step=2,
        )

    # ── STEP 2: Recibir procesos → preguntar tamaño ─────────────────
    elif session["step"] == 2:
        processes = []
        for proc in PROCESSES:
            proc_clean = proc.split(" ", 1)[1] if " " in proc else proc
            if proc_clean.lower() in lower:
                processes.append(proc)
        if not processes:
            processes = [msg]

        session["data"]["processes"] = processes
        session["step"] = 3
        return ChatResponse(
            session_id=sid,
            bot_message=(
                "Entendido. Para afinar el análisis, ¿aproximadamente "
                "**cuántos empleados** tiene tu empresa?"
            ),
            suggestions=COMPANY_SIZES,
            step=3,
        )

    # ── STEP 3: Recibir tamaño → pedir email ────────────────────────
    elif session["step"] == 3:
        size = msg
        for cs in COMPANY_SIZES:
            if cs.lower() in lower:
                size = cs
                break
        session["data"]["company_size"] = size
        session["step"] = 4
        return ChatResponse(
            session_id=sid,
            bot_message=(
                "¡Perfecto! Ya tengo todo para prepararte un análisis.\n\n"
                "Para enviarte el **reporte personalizado sin costo**, "
                "¿me compartes tu email corporativo?"
            ),
            suggestions=[],
            step=4,
        )

    # ── STEP 4: Recibir email → generar resumen y guardar lead ──────
    elif session["step"] == 4:
        email = msg if "@" in msg else f"{msg} (pendiente)"
        session["data"]["email"] = email
        session["step"] = 5

        d = session["data"]

        # Guardar lead
        lead = {
            "session_id": sid,
            "timestamp": datetime.now().isoformat(),
            "industry": d.get("industry", ""),
            "processes": d.get("processes", []),
            "company_size": d.get("company_size", ""),
            "email": email,
        }
        save_lead(lead)

        # Intentar usar LLM para el resumen; si no, usar template
        llm_response = await call_llm(
            system_prompt=(
                "Eres NovaLink Assistant, experto en automatización empresarial. "
                "Genera un resumen de análisis personalizado para un lead."
            ),
            user_message=(
                f"Industria: {d.get('industry')}\n"
                f"Procesos: {', '.join(d.get('processes', []))}\n"
                f"Tamaño: {d.get('company_size')}\n"
                f"Genera un breve análisis de automatización."
            ),
        )

        if llm_response:
            analysis = llm_response
        else:
            analysis = (
                f"📊 **Análisis preliminar para {d.get('industry', 'tu empresa')}**\n\n"
                f"🔹 **Procesos a optimizar:** {', '.join(d.get('processes', []))}\n"
                f"🔹 **Tamaño de empresa:** {d.get('company_size', '—')}\n\n"
                f"⚡ **Potencial de ahorro estimado:** 55-75% del tiempo actual\n"
                f"🔄 **Tecnologías sugeridas:** RPA + APIs + Dashboard en tiempo real\n"
                f"⏱️ **Tiempo de implementación:** 2-6 semanas\n\n"
                f"Te enviaremos el análisis completo a **{email}** en las próximas 24 horas."
            )

        return ChatResponse(
            session_id=sid,
            bot_message=(
                f"{analysis}\n\n"
                "¿Quieres que un especialista te contacte para una demo personalizada?"
            ),
            suggestions=[
                "✅ Agendar demo personalizada",
                "📧 Quiero mi reporte por email",
                "💬 Tengo otra consulta",
            ],
            step=5,
        )

    # ── STEP 5+: Conversación libre (placeholder para LLM) ──────────
    else:
        return ChatResponse(
            session_id=sid,
            bot_message=(
                "¡Gracias por tu interés! Un especialista de NovaLink te contactará pronto. "
                "Mientras tanto, ¿hay algo más en lo que pueda ayudarte?"
            ),
            suggestions=[
                "📧 Reenviar reporte",
                "🔄 Empezar de nuevo",
                "💬 Otra consulta",
            ],
            step=session["step"],
        )


# ── Main ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
