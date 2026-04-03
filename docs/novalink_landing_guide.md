# NovaLink — Guía de la Landing Page

Documento de referencia actualizado con todos los cambios implementados. Refleja el estado actual del proyecto en `index.html`.

---

## 🎨 Identidad Visual

| Elemento | Valor |
|----------|-------|
| Fondo hero / footer | Negro mate `#111111` |
| Fondo secciones | Blanco puro `#FFFFFF` |
| Fondo sección contacto | Gris claro `#F4F4F4` |
| Acento | Verde eléctrico `#20E070` (botones, iconos, bordes activos) |
| Acento oscuro (hover) | `#18b35a` |
| Texto principal | `#222222` |
| Texto secundario / descripciones | `#666666` |
| Tipografía títulos | **Inter** (700 / 900) |
| Tipografía cuerpo | **Roboto** (400 / 500) |

**Regla de uso del acento:** solo en CTAs, iconos pequeños, bordes hover y estados activos. Nunca como color de fondo de sección.

---

## 🗂️ Estructura de Archivos

```
/
├── index.html                  ← Landing page principal
├── config.js                   ← Configuración e integración Odoo CRM
└── assets/
    ├── logo/
    │   └── novalink-logo.svg   ← Logo SVG (reemplazar con versión definitiva)
    ├── icons/
    │   ├── hardware-iot.svg    ← Chip con pines (monocromático)
    │   ├── software-cloud.svg  ← Nube con flecha (monocromático)
    │   └── security.svg        ← Escudo con candado (monocromático)
    └── images/
        ├── IOT.jpg             ← Foto sección Dispositivos y Conectividad
        ├── softwaredev&cloud.jpg ← Foto sección Software & Aplicaciones
        └── security.jpg        ← Foto sección Seguridad Integral
```

> **Nota logo:** El logo en la navbar se renderiza como texto HTML (`Nova` blanco + `Link` verde). El SVG en `assets/logo/` está disponible para uso en otros materiales. Para reemplazarlo en la nav, editar directamente el HTML del `<a class="nav-logo">`.

---

## 🏗️ Estructura de la Landing Page

### 1. Navbar (fija)
- Fondo: negro con blur (`rgba(17,17,17,0.92)` + `backdrop-filter: blur`)
- Logo: texto `Nova` blanco + `Link` verde, tipografía Inter 900
- Links: Especialidad · Nosotros · Servicios
- CTA: botón verde `[Cotizar]` → ancla a `#contact`
- En mobile: links ocultos (hamburger no implementado aún)

---

### 2. Hero Section
**Enfoque:** comercial, orientado a soluciones concretas para personas no técnicas.

- **Fondo:** negro profundo con grid de puntos verdes + radial gradients sutiles
- **Badge:** `"Hogares · Empresas · Ciudades"`
- **H1:** *"Hacemos que tus espacios y negocios trabajen solos."*
- **Subtítulo:** ejemplos concretos — casa controlada desde el celular, cámaras conectadas, semáforos adaptativos. Sin mencionar IoT, Cloud ni protocolos técnicos.
- **CTAs:**
  - Primario verde: `[Quiero una solución]` → `#contact`
  - Secundario outline: `[Ver ejemplos]` → `#core`

#### Diagrama de flujo (3 nodos)
Iconos SVG inline monocromáticos color `#20E070`. Flechas también SVG outline.

| Nodo | Icono SVG | Título | Descripción |
|------|-----------|--------|-------------|
| 1 | Casa outline | Casa Inteligente | Luces, clima y puertas desde tu celular |
| 2 | Semáforo/cámara outline | Seguridad 24/7 | Cámaras y alarmas conectadas |
| 3 | Pantalla/dashboard outline | Panel de Control | Todo visible desde una sola pantalla |

---

### 3. Nuestra Especialidad (`#core`)
Fondo blanco. Grid de 3 tarjetas oscuras (`#111`) con:
- **Imagen de fondo real** (JPG) con `opacity: 0.45`, sube a `0.65` en hover
- **Overlay degradado oscuro** para mantener legibilidad del texto
- **Ícono monocromático SVG** (de `assets/icons/`) con fondo verde tenue y borde sutil
- **Hover:** borde verde + translateY(-4px)

| Tarjeta | Imagen | Ícono | Título | Descripción |
|---------|--------|-------|--------|-------------|
| 1 | `IOT.jpg` | `hardware-iot.svg` | Dispositivos y Conectividad | Sensores, cámaras y equipos que funcionan solos |
| 2 | `softwaredev&cloud.jpg` | `software-cloud.svg` | Software & Aplicaciones | Apps y paneles de control accesibles desde cualquier lugar |
| 3 | `security.jpg` | `security.svg` | Seguridad Integral | Videovigilancia, control de acceso, alarmas, seguridad residencial e industrial |

---

### 4. ¿Por qué NovaLink? (`#why`)
- Fondo negro
- Cita potente con borde izquierdo verde y fondo tenue
- 3 stats: `100%` Ciclo cubierto · `E2E` Cifrado extremo a extremo · `24/7` Soporte técnico

---

### 5. Servicios (`#services`)
Grid de 3 tarjetas outline con número grande como acento decorativo.

| # | Servicio | Descripción |
|---|----------|-------------|
| 01 | Reventa & Configuración | Equipos listos para operar desde el primer día |
| 02 | Implementación IoT | Del prototipo a la producción industrial |
| 03 | Mantenimiento Técnico | Soporte preventivo y correctivo continuo |

---

### 6. Formulario de Contacto (`#contact`)
Diseño de 2 columnas: info a la izquierda, formulario a la derecha.

**Campos:**
- Nombre completo (`id="f-name"`)
- Empresa (`id="f-company"`)
- Correo electrónico (`id="f-email"`)
- Tipo de Proyecto — dropdown (`id="f-type"`):
  - `iot` → Dispositivos / IoT / Hardware
  - `software` → Software / Aplicaciones / Cloud
  - `security` → Seguridad Integral / Videovigilancia
  - `other` → Otro
- Mensaje (`id="f-message"`)

**Integración CRM:** ver sección `config.js` más abajo.

---

### 7. Footer
Fondo negro, borde superior verde sutil. Logo HTML, copyright, links de navegación.

---

## ⚙️ config.js — Integración Odoo CRM

Archivo de configuración central. Permite activar el envío de leads al CRM sin modificar `index.html`.

### Variables principales

```js
NOVALINK_CONFIG.odoo.enabled       // false = modo demo | true = envía a Odoo
NOVALINK_CONFIG.odoo.baseUrl       // URL de tu instancia: "https://tuempresa.odoo.com"
NOVALINK_CONFIG.odoo.db            // Nombre de la base de datos
NOVALINK_CONFIG.odoo.username      // Email del usuario API
NOVALINK_CONFIG.odoo.apiKey        // API Key (Odoo → Ajustes → Técnico → Claves API)
```

### Mapeo de campos (crm.lead)

```js
fieldMap.leadName   → contact_name
fieldMap.company    → partner_name
fieldMap.email      → email_from
fieldMap.message    → description
fieldMap.stageId    → ID de etapa inicial en el pipeline
```

### Tags por tipo de proyecto
Reemplazar los `null` con los IDs reales de etiquetas en Odoo:

```js
projectTypeTags: {
  iot:      null,   // ID etiqueta "IoT / Hardware"
  software: null,   // ID etiqueta "Software / Cloud"
  security: null,   // ID etiqueta "Seguridad"
  other:    null,   // ID etiqueta "Otro"
}
```

### Para activar la integración
1. Obtener API Key en Odoo: `Ajustes → Técnico → Claves API`
2. Completar `baseUrl`, `db`, `username`, `apiKey` en `config.js`
3. Asignar IDs de etiquetas y etapa inicial
4. Cambiar `enabled: false` → `enabled: true`

> **Seguridad:** En producción, mover `apiKey` a una variable de entorno del servidor y usar un backend proxy. No exponer la clave en un repositorio público.

---

## 🛠️ Stack Técnico

| Capa | Tecnología |
|------|-----------|
| Markup | HTML5 semántico |
| Estilos | CSS puro con variables (`--accent`, `--bg-dark`, etc.) |
| Scripts | Vanilla JS (IntersectionObserver para scroll reveal, integración Odoo) |
| Fuentes | Google Fonts: Inter + Roboto |
| Despliegue | Cualquier hosting estático — Netlify, Vercel, GitHub Pages |
| Sin build step | Abrir `index.html` directamente en el navegador |

---

## 📋 Pendientes / Próximos pasos sugeridos

- [ ] Agregar menú hamburger para mobile
- [ ] Reemplazar `assets/logo/novalink-logo.svg` con isotipo/logo definitivo
- [ ] Completar IDs de etiquetas y equipo de ventas en `config.js`
- [ ] Agregar página de confirmación (`/gracias.html`) y enlazar en `redirectAfterSubmit`
- [ ] Sección de precios o paquetes
- [ ] Sección de casos de éxito / testimonios
