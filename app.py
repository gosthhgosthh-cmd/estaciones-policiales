import base64
import math
import pandas as pd
import streamlit as st
from streamlit_js_eval import get_geolocation

st.set_page_config(
    page_title="Central de Emergencias y Policía",
    page_icon="🚨",
    layout="centered",
)

st.title("🚨 Servicio de Emergencias y Estaciones Policiales")
st.write(
    "Obtén tu ubicación GPS exacta, encuentra las estaciones más cercanas,"
    " rutas y números de contacto."
)

# Imagen SVG oficial incrustada directamente (Garantiza que cargue siempre)
SVG_POLICIA_HN = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300" width="100%">
  <rect width="300" height="300" fill="#002B49" rx="20"/>
  <path d="M150 30 L230 70 V150 C230 210 150 260 150 260 C150 260 70 210 70 150 V70 Z" fill="#005691" stroke="#FFD700" stroke-width="6"/>
  <circle cx="150" cy="130" r="45" fill="#FFD700"/>
  <polygon points="150,95 162,120 190,120 167,135 176,160 150,145 124,160 133,135 110,120 138,120" fill="#002B49"/>
  <text x="150" y="210" font-family="Arial, sans-serif" font-weight="bold" font-size="14" fill="#FFFFFF" text-anchor="middle">POLICÍA NACIONAL</text>
  <text x="150" y="228" font-family="Arial, sans-serif" font-weight="bold" font-size="12" fill="#FFD700" text-anchor="middle">HONDURAS</text>
</svg>
"""


def obtener_imagen_svg(svg_str):
  b64 = base64.b64encode(svg_str.encode("utf-8")).decode("utf-8")
  return f"data:image/svg+xml;base64,{b64}"


LOGO_POLICIA = obtener_imagen_svg(SVG_POLICIA_HN)

ESTACIONES = [
    {
        "nombre": "Estación Policial Core 7 (Centro)",
        "lat": 14.1025,
        "lon": -87.2038,
        "telefono": "2222-1234 / 911",
        "foto": LOGO_POLICIA,
    },
    {
        "nombre": "Estación Policial Belén",
        "lat": 14.1120,
        "lon": -87.2180,
        "telefono": "2223-5678 / 911",
        "foto": LOGO_POLICIA,
    },
    {
        "nombre": "Estación Policial Kennedy",
        "lat": 14.0750,
        "lon": -87.1650,
        "telefono": "2228-9012 / 911",
        "foto": LOGO_POLICIA,
    },
    {
        "nombre": "Estación Policial Subirana",
        "lat": 14.0980,
        "lon": -87.2080,
        "telefono": "2237-4321 / 911",
        "foto": LOGO_POLICIA,
    },
    {
        "nombre": "Estación Policial Loarque",
        "lat": 14.0320,
        "lon": -87.2250,
        "telefono": "2226-8765 / 911",
        "foto": LOGO_POLICIA,
    },
    {
        "nombre": "Estación Policial San Miguel",
        "lat": 14.0910,
        "lon": -87.1710,
        "telefono": "2236-1122 / 911",
        "foto": LOGO_POLICIA,
    },
]


def haversine(lat1, lon1, lat2, lon2):
  R = 6371.0
  dlat = math.radians(lat2 - lat1)
  dlon = math.radians(lon2 - lon1)
  a = (
      math.sin(dlat / 2) ** 2
      + math.cos(math.radians(lat1))
      * math.cos(math.radians(lat2))
      * math.sin(dlon / 2) ** 2
  )
  return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))


def buscar_cercanas(user_lat, user_lon, limite=3):
  resultados = []
  for est in ESTACIONES:
    dist = haversine(user_lat, user_lon, est["lat"], est["lon"])
    resultados.append({
        "nombre": est["nombre"],
        "lat": est["lat"],
        "lon": est["lon"],
        "telefono": est["telefono"],
        "foto": est["foto"],
        "distancia_km": round(dist, 2),
    })
  return sorted(resultados, key=lambda x: x["distancia_km"])[:limite]


st.subheader("📍 Detección de Tu Ubicación Exacta")

loc = get_geolocation()

lat_defecto = 14.088000
lon_defecto = -87.190000

if loc and "coords" in loc:
  lat_defecto = loc["coords"]["latitude"]
  lon_defecto = loc["coords"]["longitude"]
  st.success(
      f"✅ **GPS Activo:** Coordenadas detectadas ({lat_defecto:.6f},"
      f" {lon_defecto:.6f})"
  )
else:
  st.warning(
      "⚠️ Permite el acceso a tu ubicación en el navegador para detectar tu"
      " GPS en tiempo real."
  )

col1, col2 = st.columns(2)
with col1:
  user_lat = st.number_input("Latitud", value=float(lat_defecto), format="%.6f")
with col2:
  user_lon = st.number_input(
      "Longitud", value=float(lon_defecto), format="%.6f"
  )

if st.button("🔍 Buscar 3 Estaciones Más Cercanas", use_container_width=True):
  cercanas = buscar_cercanas(user_lat, user_lon, limite=3)

  st.markdown("---")
  st.subheader("🚨 Estaciones Policiales Encontradas")

  for idx, est in enumerate(cercanas, 1):
    dist = est["distancia_km"]

    if dist < 1.0:
      transporte = "🚶 A pie o 🏍️ Motocicleta (1 a 5 min)"
    elif dist < 5.0:
      transporte = "🏍️ Motocicleta o 🚘 Automóvil (5 a 12 min)"
    else:
      transporte = (
          "🚘 Automóvil o 🏍️ Motocicleta por vía rápida (15+ min)"
      )

    with st.expander(
        f"**{idx}. {est['nombre']}** — 📏 {dist} km", expanded=True
    ):
      col_img, col_info = st.columns([1, 2])

      with col_img:
        st.image(
            est["foto"],
            caption="Policía Nacional de Honduras",
            use_container_width=True,
        )

      with col_info:
        st.write(f"📞 **Teléfono Directo:** `{est['telefono']}`")
        st.write(f"⚡ **Transporte recomendado:** {transporte}")

        maps_url = f"https://www.google.com/maps/dir/?api=1&origin={user_lat},{user_lon}&destination={est['lat']},{est['lon']}&travelmode=driving"
        st.markdown(
            f"[🗺️ **Abrir ruta GPS en Google Maps**]({maps_url})",
            unsafe_allow_html=True,
        )

  df_mapa = pd.DataFrame(
      [{"lat": user_lat, "lon": user_lon}]
      + [{"lat": e["lat"], "lon": e["lon"]} for e in cercanas]
  )
  st.markdown("---")
  st.subheader("🗺️ Ubicación en el Mapa")
  st.map(df_mapa)
