"""
NovaLink Assistant API
Backend para el chatbot de la landing page.
Flujo: Demo → Análisis gratuito → Email → Odoo CRM
"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="NovaLink Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Config ────────────────────────────────────────────────────────────

LEADS_FILE = Path(os.environ.get("LEADS_FILE", "/data/leads.json"))
LLM_API_KEY = os.environ.get("LLM_API_KEY", "")
LLM_MODEL = os.environ.get("LLM_MODEL", "deepseek-chat")
LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "https://api.deepseek.com/v1")

# ── Data ──────────────────────────────────────────────────────────────

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

# ── Session store ─────────────────────────────────────────────────────

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


# ── Odoo CRM Integration ─────────────────────────────────────────────

ODOO_URL = os.environ.get("ODOO_URL", "http://odoo:8069")
ODOO_DB = os.environ.get("ODOO_DB", "novalink")
ODOO_USERNAME = os.environ.get("ODOO_USERNAME", "")
ODOO_PASSWORD = os.environ.get("ODOO_PASSWORD", "")
ODOO_TEAM_ID = int(os.environ.get("ODOO_TEAM_ID", "1"))

import xmlrpc.client


def get_odoo_uid() -> int | None:
    """Authenticate with Odoo and return user ID."""
    try:
        common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
        return common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
    except Exception as e:
        print(f"[ODOO] Auth failed: {e}")
        return None


async def push_to_odoo(lead: dict):
    """Push lead to Odoo CRM via XML-RPC."""
    if not ODOO_USERNAME or not ODOO_PASSWORD:
        print("[ODOO] Not configured — skipping CRM push")
        return

    uid = get_odoo_uid()
    if not uid:
        return

    try:
        models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

        # Prepare lead data
        industry = lead.get("industry", "")
        processes = ", ".join(lead.get("processes", []))
        email = lead.get("email", "")

        lead_data = {
            "name": f"Lead Web — {industry}",
            "contact_name": email.split("@")[0] if "@" in email else "",
            "email_from": email if "@" in email else "",
            "description": (
                f"<p><b>Lead generado desde NovaLink Assistant</b></p>"
                f"<p><b>Industria:</b> {industry}</p>"
                f"<p><b>Procesos a optimizar:</b> {processes}</p>"
                f"<p><b>Tamaño de empresa:</b> {lead.get('company_size', '')}</p>"
                f"<p><b>Email:</b> {email}</p>"
            ),
            "type": "lead",
            "priority": "2",  # High
            "team_id": ODOO_TEAM_ID,
            "referred": "NovaLink Web Chatbot",
        }

        lead_id = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            "crm.lead", "create", [lead_data],
        )
        print(f"[ODOO] Lead creado — ID: {lead_id} — {industry} — {email}")

    except Exception as e:
        print(f"[ODOO] Error al crear lead: {e}")


# ── LLM Integration ──────────────────────────────────────────────────

NOVALINK_SYSTEM_PROMPT = """Eres NovaLink Assistant, un agente virtual experto en automatización 
empresarial para NovaLink (www.novalinkdo.com). Tu objetivo es conversar con el visitante, 
entender su negocio y mostrarle cómo la automatización puede ahorrarle tiempo y dinero.

Reglas:
- Sé cálido, profesional y entusiasta. Háblale de tú.
- Haz preguntas para entender su industria, procesos y tamaño de empresa.
- Muestra ejemplos concretos de automatización relevantes para su sector.
- Al final, ofrécele un análisis personalizado gratuito a cambio de su email.
- NO inventes precios ni garantías específicas.
- Responde en español, en 2-4 oraciones por mensaje."""


async def call_llm(system_prompt: str, user_message: str) -> str:
    """Calls LLM API. Falls back to empty string if not configured."""
    if not LLM_API_KEY:
        return ""

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
        return ""


# ── API Models ───────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    step: int = 0


class ChatResponse(BaseModel):
    session_id: str
    bot_message: str
    suggestions: list[str]
    step: int


# ── Routes ───────────────────────────────────────────────────────────

@app.get("/api/health")
def health():
    return {"status": "ok", "llm_configured": bool(LLM_API_KEY)}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    sid = req.session_id or str(uuid.uuid4())[:8]

    if sid not in sessions:
        sessions[sid] = {"step": 0, "data": {}}

    session = sessions[sid]
    msg = req.message.strip()

    # ── STEP 0: Bienvenida → Sectorizar ─────────────────────────────
    if session["step"] == 0:
        session["step"] = 1

        llm_greeting = await call_llm(
            NOVALINK_SYSTEM_PROMPT,
            "Saluda al visitante y pregúntale a qué industria pertenece su empresa. "
            "Sé breve y amigable. No des opciones, solo pregunta.",
        )

        greeting = llm_greeting or (
            "👋 ¡Hola! Soy el asistente virtual de **NovaLink**. "
            "Mi objetivo es mostrarte cómo la automatización puede transformar tu empresa "
            "en cuestión de semanas.\n\n"
            "Para empezar, ¿en qué **industria** opera tu negocio?"
        )
        return ChatResponse(
            session_id=sid,
            bot_message=greeting,
            suggestions=INDUSTRIES,
            step=1,
        )

    # ── STEP 1: Industria → Preguntar procesos ──────────────────────
    elif session["step"] == 1:
        matched = msg
        for ind in INDUSTRIES:
            ind_clean = ind.split(" ", 1)[1] if " " in ind else ind
            if ind_clean.lower() in msg.lower():
                matched = ind
                break

        session["data"]["industry"] = matched
        session["step"] = 2

        llm_resp = await call_llm(
            NOVALINK_SYSTEM_PROMPT,
            f"El visitante dice que su empresa pertenece a la industria: {matched}. "
            "Confirma que es un gran sector para automatizar (da una razón breve y concreta). "
            "Luego pregúntale qué procesos u operaciones le gustaría optimizar.",
        )

        response_text = llm_resp or (
            f"¡**{matched}**! Excelente sector para automatizar. "
            "Hemos ayudado a muchas empresas como la tuya a reducir costos operativos "
            "y eliminar tareas repetitivas.\n\n"
            "Cuéntame, ¿qué **procesos** te quitan más tiempo en el día a día? "
            "Puedes seleccionar varios o escribir lo que prefieras."
        )
        return ChatResponse(
            session_id=sid,
            bot_message=response_text,
            suggestions=PROCESSES,
            step=2,
        )

    # ── STEP 2: Procesos → Preguntar tamaño ────────────────────────
    elif session["step"] == 2:
        processes = []
        for proc in PROCESSES:
            proc_clean = proc.split(" ", 1)[1] if " " in proc else proc
            if proc_clean.lower() in msg.lower():
                processes.append(proc)
        if not processes:
            processes = [msg]

        session["data"]["processes"] = processes
        session["step"] = 3

        return ChatResponse(
            session_id=sid,
            bot_message=(
                "Entendido. Para afinar el análisis, ¿aproximadamente "
                "**cuántas personas** trabajan en tu empresa?"
            ),
            suggestions=COMPANY_SIZES,
            step=3,
        )

    # ── STEP 3: Tamaño → Output gratuito (análisis) ────────────────
    elif session["step"] == 3:
        size = msg
        for cs in COMPANY_SIZES:
            if cs.lower() in msg.lower():
                size = cs
                break

        session["data"]["company_size"] = size
        session["step"] = 4

        d = session["data"]

        llm_analysis = await call_llm(
            NOVALINK_SYSTEM_PROMPT,
            f"Genera un análisis preliminar de automatización para este perfil:\n"
            f"- Industria: {d.get('industry')}\n"
            f"- Procesos a optimizar: {', '.join(d.get('processes', []))}\n"
            f"- Tamaño de empresa: {d.get('company_size')}\n\n"
            "Estructura tu respuesta así:\n"
            "1. Un dato-impacto relevante para su sector\n"
            "2. 2-3 automatizaciones concretas que aplicarías\n"
            "3. Una estimación conservadora de tiempo ahorrado\n"
            "4. Termina pidiendo su email para enviarle el análisis completo\n"
            "Sé específico para su industria. No uses placeholders genéricos.",
        )

        if llm_analysis:
            analysis = llm_analysis
        else:
            analysis = (
                f"📊 **Análisis preliminar — {d.get('industry', 'tu empresa')}**\n\n"
                f"Basado en empresas similares que hemos ayudado, estas son las "
                f"oportunidades que detectamos:\n\n"
                f"🔹 **Procesos críticos:** {', '.join(d.get('processes', []))}\n"
                f"🔹 **Escala:** {d.get('company_size', '—')}\n\n"
                f"⚡ **Ahorro estimado:** 55-75% del tiempo actual\n"
                f"⏱️ **Tiempo de implementación:** 2-6 semanas\n"
                f"🔄 **Tecnología sugerida:** RPA + APIs + Dashboard en tiempo real\n\n"
                f"¿Te envío el **análisis completo sin costo** a tu email?"
            )

        return ChatResponse(
            session_id=sid,
            bot_message=analysis,
            suggestions=[
                "📧 Sí, enviar a mi email",
                "📞 Prefiero que me llamen",
                "💬 Tengo otra pregunta",
            ],
            step=4,
        )

    # ── STEP 4: Recibir email → Guardar lead + Odoo ────────────────
    elif session["step"] == 4:
        email = msg if "@" in msg else f"{msg} (pendiente)"
        session["data"]["email"] = email
        session["step"] = 5

        d = session["data"]

        lead = {
            "session_id": sid,
            "timestamp": datetime.now().isoformat(),
            "industry": d.get("industry", ""),
            "processes": d.get("processes", []),
            "company_size": d.get("company_size", ""),
            "email": email,
        }
        save_lead(lead)

        # Push a Odoo CRM (placeholder)
        await push_to_odoo(lead)

        return ChatResponse(
            session_id=sid,
            bot_message=(
                f"¡Perfecto! ✅ Enviaremos tu análisis completo a **{email}** "
                f"en las próximas 24 horas.\n\n"
                "Un especialista de NovaLink revisará tu caso personalmente "
                "y te contactará con recomendaciones específicas para tu empresa.\n\n"
                "¿Hay algo más en lo que pueda ayudarte mientras tanto?"
            ),
            suggestions=[
                "🔄 Empezar de nuevo",
                "📞 Quiero una demo personalizada",
                "💬 Tengo otra consulta",
            ],
            step=5,
        )

    # ── STEP 5+: Conversación libre (LLM-powered si está configurado) ──
    else:
        llm_free = await call_llm(
            NOVALINK_SYSTEM_PROMPT,
            f"El visitante dice: '{msg}'. Contexto de su sesión: {json.dumps(session['data'])}. "
            "Responde de forma útil. Si pide empezar de nuevo, indícale que sí.",
        )

        free_resp = llm_free or (
            "¡Claro! Cuéntame más sobre lo que necesitas y te ayudo "
            "a encontrar la mejor solución de automatización para tu empresa."
        )

        return ChatResponse(
            session_id=sid,
            bot_message=free_resp,
            suggestions=[
                "🔄 Empezar de nuevo",
                "📞 Agendar demo",
                "📧 Enviar análisis",
            ],
            step=session["step"],
        )


# ── Main ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
