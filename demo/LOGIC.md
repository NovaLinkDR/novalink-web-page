# LOGIC.md — Lógica del Demo Interactivo (Opción 1: Simulado)

---

## Principio Fundamental

Todo ocurre en el navegador. No hay backend, no hay APIs reales.
La lógica es una **máquina de estados** que avanza secuencialmente
a través de pasos predefinidos con delays controlados.

---

## Estructura de Datos

### Definición de un Demo

```js
const demo = {
  id: "whatsapp-ia",
  nombre: "WhatsApp IA",
  icono: "💬",
  inputPlaceholder: "Escribe un mensaje de cliente...",
  ejemplos: [
    "Quiero una cotización",
    "¿Cuál es el precio?",
    "Necesito soporte técnico"
  ],
  pasos: [ /* ver abajo */ ],
  resultado: { /* ver abajo */ }
}
```

---

### Definición de un Paso

```js
const paso = {
  id: "paso-1",
  titulo: "Mensaje recibido",
  descripcion: "El webhook de WhatsApp captura el mensaje entrante",
  servicio: "whatsapp",          // para mostrar el logo
  duracion: 800,                 // ms que tarda en "completarse"
  estado: "pendiente",           // pendiente | procesando | completado | error
  tooltipTecnico: "POST /webhook → payload: { from, body, timestamp }"
}
```

---

### Estados posibles de un paso

```
pendiente → procesando → completado
                       ↘ error (opcional, para demos avanzados)
```

---

### Definición del Resultado Final

```js
const resultado = {
  tiempoTotal: "1.8 segundos",
  tiempoManual: "~25 minutos",
  datos: [
    { etiqueta: "Lead creado", valor: "Juan Pérez — Interés: Alto" },
    { etiqueta: "Correo enviado", valor: "juan@empresa.com" },
    { etiqueta: "Tarea en CRM", valor: "Llamar en 24h" }
  ]
}
```

---

## Flujo de Ejecución

```
Usuario escribe mensaje o selecciona ejemplo
            ↓
    Clic en "Ejecutar Demo"
            ↓
    Estado global: CORRIENDO
            ↓
    Iterar sobre cada paso:
      1. Cambiar estado del paso → "procesando"
      2. Esperar paso.duracion ms
      3. Cambiar estado del paso → "completado"
      4. Pasar al siguiente paso
            ↓
    Todos los pasos completados
            ↓
    Estado global: COMPLETADO
            ↓
    Mostrar tarjeta de resultado
```

---

## Implementación en JavaScript (Vanilla)

### Máquina de estados principal

```js
// Estado global del demo
const estado = {
  demoActivo: null,       // id del demo seleccionado
  fase: "idle",           // idle | corriendo | completado
  pasoActual: 0,
  mensajeUsuario: ""
}

// Iniciar la ejecución del demo
async function ejecutarDemo(mensajeUsuario) {
  estado.mensajeUsuario = mensajeUsuario
  estado.fase = "corriendo"
  estado.pasoActual = 0

  const demo = obtenerDemoActivo()

  // Reiniciar todos los pasos a "pendiente"
  demo.pasos.forEach(paso => paso.estado = "pendiente")
  renderizarPasos(demo.pasos)

  // Ejecutar cada paso secuencialmente
  for (let i = 0; i < demo.pasos.length; i++) {
    estado.pasoActual = i
    await ejecutarPaso(demo.pasos[i])
  }

  // Mostrar resultado
  estado.fase = "completado"
  mostrarResultado(demo.resultado)
}
```

---

### Ejecución de un paso individual

```js
async function ejecutarPaso(paso) {
  // 1. Marcar como procesando
  paso.estado = "procesando"
  actualizarUI(paso)

  // 2. Esperar la duración del paso
  await esperar(paso.duracion)

  // 3. Marcar como completado
  paso.estado = "completado"
  actualizarUI(paso)

  // 4. Pequeña pausa antes del siguiente paso
  await esperar(200)
}

// Utilidad para esperar
function esperar(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}
```

---

### Actualización del DOM

```js
function actualizarUI(paso) {
  const elemento = document.getElementById(`paso-${paso.id}`)

  // Remover clases anteriores
  elemento.classList.remove("pendiente", "procesando", "completado")

  // Agregar nueva clase
  elemento.classList.add(paso.estado)

  // Actualizar ícono
  const iconos = {
    pendiente: "⬜",
    procesando: "⏳",
    completado: "✅",
    error: "❌"
  }
  elemento.querySelector(".icono-estado").textContent = iconos[paso.estado]

  // Animar conector si el paso se completó
  if (paso.estado === "completado") {
    animarConector(paso.id)
  }
}
```

---

## Datos de los Demos Predefinidos

### Demo 1: WhatsApp IA

```js
const demoWhatsApp = {
  id: "whatsapp-ia",
  pasos: [
    { id: 1, titulo: "Mensaje recibido",         servicio: "whatsapp", duracion: 600  },
    { id: 2, titulo: "Analizando con IA",         servicio: "openai",   duracion: 1200 },
    { id: 3, titulo: "Intención detectada: Ventas", servicio: "ia",     duracion: 800  },
    { id: 4, titulo: "Creando lead en CRM",       servicio: "hubspot",  duracion: 1000 },
    { id: 5, titulo: "Asignando vendedor",        servicio: "crm",      duracion: 700  },
    { id: 6, titulo: "Enviando respuesta",        servicio: "whatsapp", duracion: 900  },
    { id: 7, titulo: "Notificando al equipo",     servicio: "slack",    duracion: 600  }
  ]
}
```

### Demo 2: Procesamiento de Documentos

```js
const demoDocumentos = {
  id: "documentos",
  pasos: [
    { id: 1, titulo: "Documento recibido",        servicio: "drive",    duracion: 500  },
    { id: 2, titulo: "Extrayendo datos con OCR",  servicio: "ia",       duracion: 1500 },
    { id: 3, titulo: "Validando información",     servicio: "ia",       duracion: 900  },
    { id: 4, titulo: "Clasificando documento",    servicio: "ia",       duracion: 700  },
    { id: 5, titulo: "Creando registro en ERP",   servicio: "erp",      duracion: 1000 },
    { id: 6, titulo: "Archivando en Drive",       servicio: "drive",    duracion: 600  },
    { id: 7, titulo: "Notificando al responsable",servicio: "email",    duracion: 500  }
  ]
}
```

### Demo 3: Agendamiento Inteligente

```js
const demoAgenda = {
  id: "agenda",
  pasos: [
    { id: 1, titulo: "Solicitud recibida",        servicio: "web",      duracion: 400  },
    { id: 2, titulo: "Verificando disponibilidad",servicio: "calendar", duracion: 1000 },
    { id: 3, titulo: "Seleccionando horario",     servicio: "ia",       duracion: 800  },
    { id: 4, titulo: "Creando evento",            servicio: "calendar", duracion: 700  },
    { id: 5, titulo: "Enviando confirmación",     servicio: "email",    duracion: 600  },
    { id: 6, titulo: "Programando recordatorio",  servicio: "whatsapp", duracion: 500  }
  ]
}
```

---

## Lógica del Selector de Demo

```js
// Al cambiar de demo
function cambiarDemo(demoId) {
  // Cancelar demo en curso si existe
  if (estado.fase === "corriendo") {
    cancelarDemo()
  }

  // Actualizar demo activo
  estado.demoActivo = demoId
  estado.fase = "idle"

  // Reiniciar UI
  renderizarDemo(obtenerDemo(demoId))
}

function cancelarDemo() {
  // Limpiar todos los timeouts activos
  timeoutsActivos.forEach(id => clearTimeout(id))
  timeoutsActivos = []
  estado.fase = "idle"
}
```

---

## Lógica de Personalización del Resultado

El resultado puede variar según el mensaje del usuario para hacerlo más realista.

```js
function generarResultado(mensajeUsuario, demo) {
  // Detectar palabras clave en el mensaje
  const intencion = detectarIntencion(mensajeUsuario)

  const nombres = ["Carlos Méndez", "Ana García", "Luis Torres", "María López"]
  const nombreAleatorio = nombres[Math.floor(Math.random() * nombres.length)]

  return {
    tiempoTotal: (Math.random() * 1.5 + 1.2).toFixed(1) + " segundos",
    tiempoManual: "~" + (Math.floor(Math.random() * 20) + 15) + " minutos",
    datos: [
      { etiqueta: "Lead creado", valor: `${nombreAleatorio} — Interés: ${intencion.nivel}` },
      { etiqueta: "Categoría",   valor: intencion.categoria },
      { etiqueta: "Próxima acción", valor: intencion.accion }
    ]
  }
}

function detectarIntencion(mensaje) {
  const msg = mensaje.toLowerCase()

  if (msg.includes("precio") || msg.includes("cotización") || msg.includes("costo")) {
    return { nivel: "Alto", categoria: "Ventas", accion: "Enviar propuesta en 2h" }
  }
  if (msg.includes("soporte") || msg.includes("problema") || msg.includes("ayuda")) {
    return { nivel: "Urgente", categoria: "Soporte", accion: "Crear ticket prioritario" }
  }
  if (msg.includes("información") || msg.includes("saber")) {
    return { nivel: "Medio", categoria: "Prospecto", accion: "Enviar brochure + seguimiento" }
  }

  // Default
  return { nivel: "Medio", categoria: "General", accion: "Agendar llamada de descubrimiento" }
}
```

---

## Animaciones CSS Requeridas

```css
/* Paso en proceso: pulso */
.paso.procesando .icono-estado {
  animation: pulso 0.8s ease-in-out infinite;
}

@keyframes pulso {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.5; transform: scale(1.2); }
}

/* Paso completado: fade-in con check */
.paso.completado {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateX(-8px); }
  to   { opacity: 1; transform: translateX(0); }
}

/* Conector: llenado de arriba a abajo */
.conector {
  height: 0%;
  background: #22C55E;
  transition: height 0.4s ease;
}

.conector.activo {
  height: 100%;
}

/* Resultado: slide-up */
.resultado {
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

---

## Manejo de Errores y Edge Cases

```js
// Evitar doble ejecución
function alHacerClickEjecutar() {
  if (estado.fase === "corriendo") return  // ignorar si ya está corriendo

  const mensaje = obtenerMensajeUsuario()
  if (!mensaje.trim()) {
    mostrarError("Por favor escribe un mensaje o selecciona un ejemplo")
    return
  }

  ejecutarDemo(mensaje)
}

// Reiniciar demo
function reiniciarDemo() {
  cancelarDemo()
  ocultarResultado()
  limpiarInput()
  reiniciarPasos()
  estado.fase = "idle"
}
```

---

## Resumen del Flujo Completo

```
[Usuario] → Selecciona demo
         → Escribe mensaje o elige ejemplo
         → Clic en "Ejecutar"
              ↓
[Sistema] → Valida input
          → Cambia fase a "corriendo"
          → Loop de pasos:
              → paso.estado = "procesando" → render → esperar → paso.estado = "completado" → render
          → Genera resultado personalizado
          → Muestra tarjeta de resultado
          → Fase = "completado"
              ↓
[Usuario] → Puede reiniciar o cambiar de demo
```

---

## Tecnologías Recomendadas

| Necesidad              | Opción simple       | Opción avanzada       |
|------------------------|---------------------|-----------------------|
| Framework UI           | Vanilla JS + CSS    | React + Framer Motion |
| Animaciones            | CSS Animations      | GSAP / Framer Motion  |
| Íconos de servicios    | SVG inline          | Simple Icons (npm)    |
| Confetti al finalizar  | canvas-confetti     | tsParticles           |
| Hosting                | Vercel / Netlify    | Vercel + CDN          |

---

## Notas Finales

- Todo el estado vive en memoria del navegador. No se necesita servidor.
- Los datos del resultado son generados aleatoriamente en cada ejecución para que se vea dinámico.
- El demo debe poder reiniciarse ilimitadas veces sin recargar la página.
- Agregar un botón "Ver código técnico" que muestre el pseudocódigo del flujo puede aumentar la credibilidad ante perfiles técnicos.