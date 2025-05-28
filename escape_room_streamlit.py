
import streamlit as st

# ---------------------- Objetos del juego ---------------------- #

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
double_bed = {"name": "double_bed", "type": "furniture"}
queen_bed = {"name": "queen_bed", "type": "furniture"}
dresser = {"name": "dresser", "type": "furniture"}
dining_table = {"name": "dining_table", "type": "furniture"}

# Habitaciones
game_room = {"name": "game_room", "type": "room"}
bedroom_1 = {"name": "bedroom_1", "type": "room"}
bedroom_2 = {"name": "bedroom_2", "type": "room"}
living_room = {"name": "living_room", "type": "room"}
congratulations = {"name": "congratulations", "type": "room"}

# Relaciones
object_relations = {
    "game_room": [couch, piano, door_a],
    "piano": [key_a],
    "bedroom_1": [queen_bed, door_a, door_b],
    "queen_bed": [key_b],
    "bedroom_2": [double_bed, dresser, door_b, door_c],
    "dresser": [key_c],
    "living_room": [dining_table, door_c, door_d],
    "dining_table": [key_d],
    "congratulations": [],
    "door_a": [game_room, bedroom_1],
    "door_b": [bedroom_1, bedroom_2],
    "door_c": [bedroom_2, living_room],
    "door_d": [living_room, congratulations]
}

INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "target_room": congratulations
}

# ---------------------- Inicialización ---------------------- #

if 'current_room' not in st.session_state:
    st.session_state.current_room = INIT_GAME_STATE["current_room"]
    st.session_state.keys_collected = []

# ---------------------- Funciones ---------------------- #

def get_objects_in_room(room):
    return object_relations.get(room["name"], [])

def examine_object(obj):
    if obj["type"] == "furniture":
        items = object_relations.get(obj["name"], [])
        if items:
            key = items[0]
            if key not in st.session_state.keys_collected:
                st.session_state.keys_collected.append(key)
                st.success(f"¡Encontraste una llave!: {key['name']}")
            else:
                st.info("Ya revisaste este objeto.")
        else:
            st.warning("No encontraste nada.")
    elif obj["type"] == "door":
        try_to_unlock_door(obj)

def try_to_unlock_door(door):
    for key in st.session_state.keys_collected:
        if key["target"] == door:
            next_room = [room for room in object_relations[door["name"]] if room != st.session_state.current_room][0]
            st.session_state.current_room = next_room
            st.success(f"Abriste la {door['name']} y entraste a {next_room['name']}.")
            return
    st.error("La puerta está cerrada. Necesitas la llave correcta.")

# ---------------------- Interfaz ---------------------- #

st.title("🔐 Escape Room Completo")
room = st.session_state.current_room
st.subheader(f"Estás en: **{room['name']}**")

# Mostrar objetos
for obj in get_objects_in_room(room):
    if st.button(f"Explorar {obj['name']}"):
        examine_object(obj)

# Victoria
if room == congratulations:
    st.balloons()
    st.success("🎉 ¡Felicidades! Has escapado del juego.")
