"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from src.recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    print(f"Loaded {len(songs)} songs.")

    high_energy_pop = {"genre": "pop", "mood": "happy", "energy": 0.85, "valence": 0.80, "danceability": 0.80, "tempo_bpm": 125, "acousticness": 0.10}
    chill_lofi      = {"genre": "lofi", "mood": "chill", "energy": 0.35, "valence": 0.55, "danceability": 0.55, "tempo_bpm": 75, "acousticness": 0.80}
    deep_rock       = {"genre": "rock", "mood": "intense", "energy": 0.90, "valence": 0.45, "danceability": 0.65, "tempo_bpm": 150, "acousticness": 0.08}

    # Adversarial / edge-case profiles
    conflicting     = {"genre": "pop", "mood": "sad", "energy": 0.90, "valence": 0.80, "danceability": 0.85, "tempo_bpm": 130, "acousticness": 0.10}
    no_mood_match   = {"genre": "pop", "mood": "melancholic", "energy": 0.60, "valence": 0.50, "danceability": 0.55, "tempo_bpm": 100, "acousticness": 0.30}

    profiles = [
        ("High-Energy Pop",               high_energy_pop),
        ("Chill Lofi",                     chill_lofi),
        ("Deep Intense Rock",              deep_rock),
        ("Adversarial: Conflicting Prefs", conflicting),
        ("Adversarial: No Mood Match",     no_mood_match),
    ]

    col_w = 55

    def profile_block(label, prefs):
        recs = recommend_songs(prefs, songs, k=5)
        lines = [f"  PROFILE: {label}", "-" * col_w]
        for i, (song, score, explanation) in enumerate(recs, start=1):
            lines.append(f"  #{i} {song['title']} by {song['artist']}")
            lines.append(f"     Score: {score:.2f}")
            for reason in explanation.split(", "):
                lines.append(f"       - {reason}")
        return lines

    profile_blocks = [profile_block(label, prefs) for label, prefs in profiles]

    for i in range(0, len(profile_blocks), 2):
        left  = profile_blocks[i]
        right = profile_blocks[i + 1] if i + 1 < len(profile_blocks) else []
        print("\n" + "=" * (col_w * 2 + 4))
        rows = max(len(left), len(right))
        for r in range(rows):
            l  = left[r]  if r < len(left)  else ""
            ri = right[r] if r < len(right) else ""
            print(f"{l:<{col_w}}  {ri}")
    print("=" * (col_w * 2 + 4))


if __name__ == "__main__":
    main()
