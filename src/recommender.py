from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by compatibility with the given user profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended for a user."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        songs = []
        for row in reader:
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            songs.append(row)
        return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    # Categorical: genre (weight 0.40)
    if song.get('genre') == user_prefs.get('genre'):
        score += 0.40
        reasons.append("genre match (+0.40)")

    # Categorical: mood (weight 0.30)
    if song.get('mood') == user_prefs.get('mood'):
        score += 0.30
        reasons.append("mood match (+0.30)")

    # Numerical: similarity = 1 - |target - value| / range, clamped to [0, 1]
    def num_score(target, value, range_val, weight, label):
        sim = max(0.0, 1.0 - abs(target - value) / range_val)
        contribution = sim * weight
        return contribution, f"{label} similarity {sim:.2f} (+{contribution:.2f})"

    if 'energy' in user_prefs:
        pts, reason = num_score(user_prefs['energy'], song['energy'], 1.0, 0.10, "energy")
        score += pts
        reasons.append(reason)

    if 'valence' in user_prefs:
        pts, reason = num_score(user_prefs['valence'], song['valence'], 1.0, 0.10, "valence")
        score += pts
        reasons.append(reason)

    if 'danceability' in user_prefs:
        pts, reason = num_score(user_prefs['danceability'], song['danceability'], 1.0, 0.05, "danceability")
        score += pts
        reasons.append(reason)

    if 'tempo_bpm' in user_prefs:
        pts, reason = num_score(user_prefs['tempo_bpm'], song['tempo_bpm'], 92.0, 0.03, "tempo_bpm")
        score += pts
        reasons.append(reason)

    if 'acousticness' in user_prefs:
        pts, reason = num_score(user_prefs['acousticness'], song['acousticness'], 1.0, 0.02, "acousticness")
        score += pts
        reasons.append(reason)

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [
        (song, *score_song(user_prefs, song))
        for song in songs
    ]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return [(song, score, ", ".join(reasons)) for song, score, reasons in ranked[:k]]
