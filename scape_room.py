
import streamlit as st

# ---------- Objetos y Estado del Juego ---------- #

# Puertas
door_a = {"name": "door_a", "type": "door"}
door_b = {"name": "door_b", "type": "door"}
door_c = {"name": "door_c", "type": "door"}
door_d = {"name": "door_d", "type": "door"}

# Llaves
key_a = {"name": "key for door a", "type": "key", "target": door_a}
key_b = {"name": "key for door b", "type": "key", "target": door_b}
key_c = {"name": "key for door c", "type": "key", "target": door_c}
key_d = {"name": "key for door d", "type": "key", "target": door_d}

# Muebles
couch = {"name": "couch", "type": "furniture"}
piano = {"name": "piano", "type": "furniture"}

# Habitaciones
game_room = {"name": "game_room", "type": "room"}
congratulations = {"name": "congratulations", "type": "room"}

# Relaciones
object_relations = {
    "game_room": [couch, piano, door_a],
    "piano": [key_a]
}

# Estado del juego
if 'current_room' not in st.session_state:
    st.session_state.current_room = game_room
    st.session_state.keys_collected = []

# ---------- Funciones ---------- #

def get_objects_in_room(room):
    return object_relations.get(room["name"], [])

def examine_object(obj):
    if obj["type"] == "furniture":
        items = object_relations.get(obj["name"], [])
        if items:
            key = items[0]
            st.session_state.keys_collected.append(key)
            st.success(f"¡Encontraste una llave!: {key['name']}")
        else:
            st.warning("No encontraste nada.")
    elif obj["type"] == "door":
        for key in st.session_state.keys_collected:
            if key["target"] == obj:
                st.session_state.current_room = congratulations
                st.success("¡Abriste la puerta y ganaste!")
                return
        st.error("La puerta está cerrada. Necesitas una llave.")

# ---------- Interfaz ---------- #

st.title("🔐 Escape Room - Versión Streamlit")
st.write(f"Estás en: **{st.session_state.current_room['name']}**")

objects_here = get_objects_in_room(st.session_state.current_room)

for obj in objects_here:
    if st.button(f"Inspeccionar {obj['name']}"):
        examine_object(obj)

if st.session_state.current_room == congratulations:
    st.balloons()
    st.subheader("¡Felicidades! Has escapado.")
