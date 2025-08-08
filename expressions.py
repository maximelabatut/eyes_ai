expressions = {
    "normal": {
        "left_eye": {"pupil_pos": (0, 0), "eyelid_top": 0, "eyelid_bottom": 0},
        "right_eye": {"pupil_pos": (0, 0), "eyelid_top": 0, "eyelid_bottom": 0},
        "mouth": {"shape": "straight", "width": 80, "height": 5}
    },
    "happy": {
        "left_eye": {"pupil_pos": (0, 10), "eyelid_top": 20, "eyelid_bottom": 20},
        "right_eye": {"pupil_pos": (0, 10), "eyelid_top": 20, "eyelid_bottom": 20},
        # Même largeur et hauteur que sad, juste forme différente
        "mouth": {"shape": "smile", "width": 80, "height": 30}
    },
    "sad": {
        "left_eye": {"pupil_pos": (0, -10), "eyelid_top": -10, "eyelid_bottom": -10},
        "right_eye": {"pupil_pos": (0, -10), "eyelid_top": -10, "eyelid_bottom": -10},
        "mouth": {"shape": "frown", "width": 80, "height": 30}
    }
}
