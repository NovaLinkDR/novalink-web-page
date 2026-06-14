# DESIGN.md — Demo Interactivo de Automatización (Opción 1: Simulado)

---

## Concepto General

Una sección en la página web que simula visualmente una automatización completa en tiempo real.
El visitante interactúa, ve el flujo ejecutarse paso a paso, y entiende el valor del servicio en menos de 60 segundos.

---

## Layout General

```
┌─────────────────────────────────────────────────────────┐
│                    HERO / TÍTULO                        │
│     "Mira cómo automatizamos tu negocio en vivo"        │
│         [Selector de tipo de demo]                      │
├──────────────────────┬──────────────────────────────────┤
│                      │                                  │
│   PANEL IZQUIERDO    │       PANEL DERECHO              │
│   (Input del usuario)│       (Flujo visual animado)     │
│                      │                                  │
└──────────────────────┴──────────────────────────────────┘
│                  RESULTADO FINAL                        │
│         (Tarjeta con resumen + CTA)                     │
└─────────────────────────────────────────────────────────┘
```

---

## Sección 1: Selector de Demo

El usuario elige qué tipo de automatización quiere ver.

```
┌──────────────────────────────────────────────────────────┐
│  ¿Qué automatización quieres ver?                        │
│                                                          │
│  [ 💬 WhatsApp IA ]  [ 📄 Documentos ]  [ 📅 Agenda ]   │
│  [ 📧 Email + CRM ]  [ 🧾 Propuestas ]                   │
└──────────────────────────────────────────────────────────┘
```

- Tabs o botones tipo pill.
- El seleccionado se resalta con color primario.
- Al cambiar, el demo se reinicia.

---

## Sección 2: Panel Izquierdo — Input del Usuario

Simula el punto de entrada de la automatización.

### Ejemplo: Demo de WhatsApp IA

```
┌─────────────────────────────────┐
│  📱 Simula un mensaje           │
│                                 │
│  ┌───────────────────────────┐  │
│  │ Escribe tu mensaje...     │  │
│  └───────────────────────────┘  │
│                                 │
│  O elige un ejemplo:            │
│  [ "Quiero una cotización" ]    │
│  [ "¿Cuál es el precio?" ]      │
│  [ "Necesito soporte" ]         │
│                                 │
│       [ ▶ Ejecutar Demo ]       │
└─────────────────────────────────┘
```

- Input de texto libre o botones de ejemplo predefinidos.
- Botón principal con color llamativo.
- Al hacer clic, se activa la animación del flujo.

---

## Sección 3: Panel Derecho — Flujo Visual Animado

Muestra los pasos de la automatización ejecutándose uno a uno.

```
┌──────────────────────────────────────────────┐
│  🔄 Automatización en progreso...            │
│                                              │
│  ✅ Mensaje recibido                         │
│     │                                        │
│  ⏳ Analizando intención con IA...           │
│     │                                        │
│  ⏳ Clasificando como: Ventas                │
│     │                                        │
│  ⏳ Creando lead en CRM...                   │
│     │                                        │
│  ⏳ Asignando vendedor...                    │
│     │                                        │
│  ⏳ Enviando respuesta automática...         │
│     │                                        │
│  ⏳ Notificando al equipo por Slack...       │
│                                              │
└──────────────────────────────────────────────┘
```

### Comportamiento visual de cada paso:

| Estado     | Ícono | Color       | Animación              |
|------------|-------|-------------|------------------------|
| Pendiente  | ⬜    | Gris        | Ninguna                |
| En proceso | ⏳    | Amarillo    | Pulso / spinner        |
| Completado | ✅    | Verde       | Check con fade-in      |
| Error      | ❌    | Rojo        | Shake suave            |

- Los pasos aparecen secuencialmente con un delay de 800ms–1200ms entre cada uno.
- La línea vertical que conecta los pasos se va "llenando" como una barra de progreso.
- Cada paso tiene un ícono del servicio (WhatsApp, CRM, Slack, etc.).

---

## Sección 4: Resultado Final

Aparece cuando todos los pasos se completan.

```
┌──────────────────────────────────────────────────────┐
│  🎉 ¡Automatización completada!                      │
│                                                      │
│  ⏱ Tiempo total: 1.8 segundos                       │
│  👤 Lead creado: Juan Pérez — Interés: Alto          │
│  📧 Correo enviado a: juan@empresa.com               │
│  📋 Tarea creada en CRM: "Llamar en 24h"             │
│                                                      │
│  Sin automatización esto tomaría: ~25 minutos        │
│                                                      │
│  [ 🚀 Quiero esto para mi empresa ]                  │
│  [ 🔄 Probar otro demo ]                             │
└──────────────────────────────────────────────────────┘
```

- Aparece con una animación de entrada (slide-up o fade).
- Muestra datos ficticios pero realistas.
- CTA principal bien visible.

---

## Paleta de Colores Sugerida

| Elemento              | Color sugerido         |
|-----------------------|------------------------|
| Fondo principal       | `#0F172A` (dark navy)  |
| Fondo de paneles      | `#1E293B`              |
| Color primario        | `#6366F1` (indigo)     |
| Paso completado       | `#22C55E` (verde)      |
| Paso en proceso       | `#FACC15` (amarillo)   |
| Texto principal       | `#F8FAFC`              |
| Texto secundario      | `#94A3B8`              |
| Borde de tarjetas     | `#334155`              |

---

## Tipografía Sugerida

- **Títulos:** Inter Bold o Geist Bold
- **Cuerpo:** Inter Regular
- **Código / datos:** JetBrains Mono o Fira Code

---

## Componentes UI Clave

### Tarjeta de paso (Step Card)
```
┌────────────────────────────────────────┐
│  [ícono servicio]  Nombre del paso     │
│                    Descripción breve   │
│                              [✅ / ⏳] │
└────────────────────────────────────────┘
```

### Conector animado entre pasos
- Línea vertical punteada que se convierte en sólida al completarse.
- Color: gris → verde al completar.

### Badge de servicio
- Pequeño chip con logo e ícono del servicio.
- Ejemplos: WhatsApp (verde), Gmail (rojo), Slack (morado), HubSpot (naranja).

---

## Responsividad

| Pantalla     | Layout                                      |
|--------------|---------------------------------------------|
| Desktop      | Dos columnas (input izquierda, flujo derecha)|
| Tablet       | Dos columnas compactas                      |
| Mobile       | Una columna, input arriba, flujo abajo      |

---

## Microinteracciones Importantes

1. **Al hacer clic en "Ejecutar Demo":**
   - Botón muestra spinner por 300ms.
   - Luego inicia la secuencia de pasos.

2. **Al completar cada paso:**
   - Sonido sutil opcional (tick).
   - El ícono cambia de ⏳ a ✅ con animación.

3. **Al completar todo el flujo:**
   - Confetti o partículas suaves.
   - Tarjeta de resultado aparece con slide-up.

4. **Al pasar el cursor sobre un paso:**
   - Tooltip con descripción técnica del paso.
   - Ejemplo: "Webhook recibido → n8n procesa → HubSpot API"

---

## Notas de Diseño

- Mantener el demo **por encima del fold** en desktop.
- El flujo debe verse **técnico pero entendible** para no-técnicos.
- Usar logos reales de herramientas conocidas (Zapier, Make, HubSpot, Slack) para generar credibilidad.
- Incluir un contador de "Tiempo ahorrado" que suba en tiempo real durante la demo.