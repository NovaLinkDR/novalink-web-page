/**
 * NovaLink — Configuración de integración con Odoo CRM
 *
 * Para activar la integración, completa los valores marcados con TODO
 * y establece ODOO_ENABLED = true.
 *
 * Documentación de la API JSON-RPC de Odoo:
 * https://www.odoo.com/documentation/17.0/developer/reference/external_api.html
 */

const NOVALINK_CONFIG = {

  /* ── INTEGRACIÓN ODOO CRM ──────────────────────────────────────────── */
  odoo: {
    /**
     * Activa o desactiva el envío de leads al CRM.
     * false → solo simula el envío (modo demo / desarrollo).
     * true  → envía datos reales a tu instancia de Odoo.
     */
    enabled: false,

    /** URL base de tu instancia Odoo. Ej: "https://miempresa.odoo.com" */
    baseUrl: "https://TU_INSTANCIA.odoo.com",

    /** Nombre de la base de datos Odoo */
    db: "TU_BASE_DE_DATOS",

    /** Usuario con acceso a la API (normalmente el email del admin) */
    username: "admin@tuempresa.com",

    /**
     * API Key generada en Odoo: Ajustes → Técnico → Claves API.
     * NUNCA expongas esta clave en un repositorio público.
     * En producción, mueve este valor a una variable de entorno del servidor.
     */
    apiKey: "TU_API_KEY_ODOO",

    /* ── Mapeo de campos del formulario → campos del Lead en Odoo ─── */
    fieldMap: {
      /** crm.lead: nombre del cliente potencial */
      leadName:    "contact_name",

      /** crm.lead: nombre de la empresa */
      company:     "partner_name",

      /** crm.lead: correo electrónico */
      email:       "email_from",

      /** crm.lead: campo de texto libre para el mensaje */
      message:     "description",

      /**
       * crm.lead: origen de la campaña / medio.
       * Se mapea al campo "source_id" (requiere ID de registro en Odoo).
       * Puedes dejarlo en null para no asignar origen automáticamente.
       */
      source:      "source_id",

      /**
       * crm.lead: etapa inicial del pipeline.
       * Busca el ID de la etapa "Nuevo" en tu instancia:
       * Odoo → CRM → Configuración → Etapas.
       */
      stageId:     1,
    },

    /* ── Mapeo de tipos de proyecto → etiquetas (tag_ids) en Odoo ── */
    projectTypeTags: {
      /**
       * Cada valor debe ser el ID de la etiqueta en tu Odoo.
       * Odoo → CRM → Configuración → Etiquetas.
       */
      iot:       null,   // TODO: reemplaza con el ID de la etiqueta "IoT / Hardware"
      software:  null,   // TODO: reemplaza con el ID de la etiqueta "Software / Cloud"
      security:  null,   // TODO: reemplaza con el ID de la etiqueta "Seguridad"
      other:     null,   // TODO: reemplaza con el ID de la etiqueta "Otro"
    },

    /** Equipo de ventas al que se asignará el lead (team_id). null = sin asignar. */
    salesTeamId: null,

    /** Usuario responsable por defecto (user_id). null = sin asignar. */
    defaultUserId: null,
  },

  /* ── FORMULARIO DE CONTACTO ─────────────────────────────────────── */
  form: {
    /**
     * Mensaje de éxito mostrado al usuario después de enviar.
     */
    successMessage: "¡Solicitud recibida! Te contactaremos en menos de 24 horas.",

    /**
     * Mensaje de error genérico.
     */
    errorMessage: "Hubo un problema al enviar tu solicitud. Por favor intenta de nuevo.",

    /**
     * Redirigir al usuario a una URL de "gracias" después del envío.
     * null = no redirigir (muestra el mensaje en la misma página).
     */
    redirectAfterSubmit: null, // ej: "/gracias.html"
  },

  /* ── INFORMACIÓN DE LA EMPRESA (uso interno en plantillas) ──────── */
  company: {
    name:    "NovaLink",
    email:   "contacto@novalink.io",
    phone:   "+52 000 000 0000",
    website: "https://novalink.io",
  },
};

/* ── Función auxiliar: envío del formulario ────────────────────────── */

/**
 * Envía los datos del formulario a Odoo via JSON-RPC.
 * Si odoo.enabled = false, simula el envío en consola.
 *
 * @param {Object} formData
 * @param {string} formData.name        - Nombre del contacto
 * @param {string} formData.company     - Empresa
 * @param {string} formData.email       - Correo electrónico
 * @param {string} formData.projectType - Tipo de proyecto (iot|software|security|other)
 * @param {string} formData.message     - Mensaje libre
 * @returns {Promise<{ok: boolean, message: string}>}
 */
async function submitToOdoo(formData) {
  const cfg = NOVALINK_CONFIG.odoo;

  if (!cfg.enabled) {
    console.info("[NovaLink] Modo demo — datos que se enviarían a Odoo:", formData);
    return { ok: true, message: NOVALINK_CONFIG.form.successMessage };
  }

  const tagId = cfg.projectTypeTags[formData.projectType] ?? null;

  const leadValues = {
    [cfg.fieldMap.leadName]:  formData.name,
    [cfg.fieldMap.company]:   formData.company,
    [cfg.fieldMap.email]:     formData.email,
    [cfg.fieldMap.message]:   formData.message,
    stage_id:                  cfg.fieldMap.stageId,
    ...(tagId              && { tag_ids: [[4, tagId]] }),
    ...(cfg.salesTeamId    && { team_id: cfg.salesTeamId }),
    ...(cfg.defaultUserId  && { user_id: cfg.defaultUserId }),
  };

  try {
    const response = await fetch(`${cfg.baseUrl}/web/dataset/call_kw`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        jsonrpc: "2.0",
        method:  "call",
        params: {
          model:  "crm.lead",
          method: "create",
          args:   [leadValues],
          kwargs: {
            context: {
              lang:         "es_MX",
              allowed_company_ids: [1],
            },
          },
        },
      }),
    });

    const json = await response.json();

    if (json.error) {
      console.error("[NovaLink] Error Odoo:", json.error);
      return { ok: false, message: NOVALINK_CONFIG.form.errorMessage };
    }

    return { ok: true, message: NOVALINK_CONFIG.form.successMessage };

  } catch (err) {
    console.error("[NovaLink] Error de red:", err);
    return { ok: false, message: NOVALINK_CONFIG.form.errorMessage };
  }
}
