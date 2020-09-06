faces = {
    "face_grinning": "😀",
    "face_grinning_with_eyes": "😄",
    "face_beaming_with_eyes": "😁",
    "face_grinning_squinting": "😆",
    "face_grinning_with_sweat": "😅",

    "face_laughing_out_loud": "🤣",
    "face_with_tears_of_joy": "😂",
    "face_slightly_smiling": "🙂",
    "face_winking": "😉",
    "face_with_smiling_eyes": "😊",

    "face_with_heart_eyes": "😍",
    "face_blowing_kiss": "😘",
    "face_with_tounge_out": "😋",
    "face_winking_with_tounge_out": "😜",
    "face_zany": "🤪",

    "face_with_raised_eyebrow": "🤨",
    "face_expressionless": "😑",
    "face_unamused": "😒",
    "face_with_rolling_eyes": "🙄",
    "face_grimacing": "😬",

    "face_pensive": "😔",
    "face_sleepy": "😪",
    "face_sleeping": "😴",
    "face_with_thermometer": "🤒",
    "face_sneezing": "🤧",

    "face_dizzy": "😵",
    "face_worried": "😟",
    "face_astonished": "😲",
    "face_sad_but_relieved": "😥",
    "face_loudly_crying": "😭",

    "face_confounded": "😖",
    "face_downcast_with_sweat": "😓",
    "face_weary": "😩",
    "face_with_steam_from_nose": "😤",
    "face_angry": "😠",

    "face_robot": "🤖",
    "face_alien": "👽",
    "face_ghost": "👻",
    "face_ogre": "👹",
    "face_clown": "🤡"
}

animals = {
    "animal_monkey": "🐒",
    "animal_gorilla": "🦍",
    "animal_orangutan": "🦧",

    "animal_dog": "🐕",
    "animal_guide_dog": "🦮",
    "animal_poodle": "🐩",
    "animal_woolf": "🐺",
    "animal_fox": "🦊",
    "animal_raccoon": "🦝",

    "animal_cat": "🐈",
    "animal_lion": "🦁",
    "animal_tiger": "🐅",
    "animal_leopard": "🐆",

    "animal_horse": "🐎",
    "animal_unicorn": "🦄",
    "animal_zebra": "🦓",
    "animal_deer": "🦌",

    "animal_cow": "🐄",
    "animal_ox": "🐂",
    "animal_water_buffalo": "🐃",

    "animal_pig": "🐖",
    "animal_boar": "🐗",

    "animal_ram": "🐏",
    "animal_ewe": "🐑",
    "animal_goat": "🐐",
    "animal_camel": "🐪",
    "animal_llama": "🦙",

    "animal_giraffe": "🦒",
    "animal_elephant": "🐘",
    "animal_rhinoceros": "🦏",
    "animal_hippopatamus": "🦛",

    "animal_mouse": "🐁",
    "animal_hamster": "🐹",
    "animal_rabbit": "🐇",
    "animal_chipmunk": "🐿️",
    "animal_hedgehog": "🦔",
    "animal_bat": "🦇",

    "animal_bear": "🐻",
    "animal_koala": "🐨",
    "animal_panda": "🐼",
    "animal_sloth": "🦥",

    "animal_otter": "🦦",
    "animal_skunk": "🦨",
    "animal_kangaroo": "🦘",
    "animal_badger": "🦡",

    "animal_turkey": "🦃",
    "animal_chicken": "🐔",
    "animal_chick": "🐤",
    "animal_bird": "🐦",
    "animal_penguin": "🐧",
    "animal_dove": "🕊️",
    "animal_eagle": "🦅",
    "animal_duck": "🦆",
    "animal_swan": "🦢",
    "animal_owl": "🦉",
    "animal_flamingo": "🦩",
    "animal_peacock": "🦚",
    "animal_parrot": "🦜",

    "animal_frog": "🐸",
    "animal_crocodile": "🐊",
    "animal_turtle": "🐢",
    "animal_lizard": "🦎",
    "animal_snake": "🐍",
    "animal_dragon": "🐉",

    "animal_sauropod": "🦕",
    "animal_t_rex": "🦖",

    "animal_whale": "🐋",
    "animal_dolphin": "🐬",
    "animal_fish": "🐟",
    "animal_tropical_fish": "🐠",
    "animal_blowfish": "🐡",
    "animal_shark": "🦈",
    "animal_octopus": "🐙",

    "animal_snail": "🐌",
    "animal_butterfly": "🦋",
    "animal_bug": "🐛",
    "animal_ant": "🐜",
    "animal_honeybee": "🐝",
    "animal_ladybug": "🐞",
    "animal_cricket": "🦗",
    "animal_spider": "🕷️",
    "animal_scorpion": "🦂",
    "animal_mosquito": "🦟"
}

def get_emojis(to_get=None):
    """Return a dictionary with emojis. This is a function so as not to
    waste memory if not neccessary.
    """
    to_get = to_get or ["faces", "animals"]
    emojis_map = {"faces": faces, "animals": animals}

    result = {}
    for category in to_get:
        try:
            result.update(emojis_map[category])
        except KeyError:
            raise ValueError(f"The category '{category}' does not exist")

    return result

def list_emojis(to_get=None):
    """A generator which returns a new emoji from all emojis"""
    emojis_to_list = get_emojis(to_get)
    for name, emoji in emojis_to_list.items():
        yield emoji
