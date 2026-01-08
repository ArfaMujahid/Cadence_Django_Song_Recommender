import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

def get_recommendations(song_name, artist_name):
    recommendations = []

    # Feature Engineering
    # Get the absolute path to the CSV file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "songs.csv")
    df = pd.read_csv(csv_path)
    # Check for missing values
    missing_values = df.isnull().sum()
    if missing_values.any():
        print("Warning: Dataset contains missing values")

    # Create song identifier
    df["song"] = df["track_name"] + " - " + df["artist_name"]

    # drops the columns 'lyrics' and 'len' from the df
    df.drop(["lyrics", "len"], axis=1, inplace=True)

    # Applying one-hot encoding to the categorical columns
    df = pd.get_dummies(df, columns=["topic", "artist_name", "genre"])

    # Scale release_date
    scaler = MinMaxScaler()
    df["release_date"] = scaler.fit_transform(df[["release_date"]])

    topic_genre_columns = [
        col for col in df.columns if col.startswith("topic") or col.startswith("genre")
    ]

    # Custom similarity function
    def custom_similarity(song1, song2):
        features_song1 = np.array(
            [song1["release_date"]] + [song1[col] for col in topic_genre_columns]
        )
        features_song2 = np.array(
            [song2["release_date"]] + [song2[col] for col in topic_genre_columns]
        )
        distance = np.linalg.norm(features_song1 - features_song2)
        return distance

    def find_song_index(song_name):
        return df.index[df["song"] == song_name].tolist()

    input_song_name = song_name + " - " + artist_name
    input_song_index = find_song_index(input_song_name)

    if not input_song_index:
        print("Song not found.")
        return []

    input_song_index = input_song_index[0]
    input_song_features = df.iloc[input_song_index]

    # Custom similarity method
    similarity_scores = []
    for i in range(len(df)):
        song_name = df.iloc[i]["song"]
        similarity_score = custom_similarity(input_song_features, df.iloc[i])
        similarity_scores.append((song_name, similarity_score))

    sorted_similarity_scores = sorted(similarity_scores, key=lambda x: x[1])
    recommended_songs = [
        song_name for song_name, similarity_score in sorted_similarity_scores
    ]

    # Get top 20 from custom similarity
    for index, song_name in enumerate(recommended_songs[:20]):
        recommendations.append(song_name)

    # First KNN layer based upon context
    first_knn_columns = [
        "dating",
        "violence",
        "world/life",
        "night/time",
        "shake the audience",
        "family/gospel",
        "romantic",
        "communication",
        "obscene",
        "music",
        "movement/places",
        "light/visual perceptions",
        "family/spiritual",
        "like/girls",
        "sadness",
        "feelings",
    ]
    X_first_knn = df[first_knn_columns]
    first_knn = NearestNeighbors(n_neighbors=101)
    first_knn.fit(X_first_knn)

    input_song_neighbors_first = first_knn.kneighbors(
        [X_first_knn.iloc[input_song_index]], return_distance=False
    )[0]

    # Second KNN layer based upon the musical factors
    second_knn_columns = [
        "danceability",
        "loudness",
        "acousticness",
        "instrumentalness",
        "valence",
        "energy",
    ]

    X_second_knn = df.iloc[input_song_neighbors_first][second_knn_columns]
    second_knn = NearestNeighbors(n_neighbors=21)
    second_knn.fit(X_second_knn)

    input_song_neighbors_second = second_knn.kneighbors(
        [X_second_knn.iloc[0]], return_distance=False
    )[0]

    # Get top 20 from KNN
    for i, song_index in enumerate(input_song_neighbors_second):
        song_name = df.iloc[song_index]["song"]
        if song_name not in recommendations:
            recommendations.append(song_name)

    # Custom KNN implementation
    def knn(X, query_point, k=5):
        distances = []
        for i in range(len(X)):
            distance = np.linalg.norm(X[i] - query_point)
            distances.append((i, distance))
        sorted_distances = sorted(distances, key=lambda x: x[1])
        nearest_neighbors_indices = [x[0] for x in sorted_distances[:k]]
        return nearest_neighbors_indices

    X_first_knn = df[first_knn_columns].values
    X_second_knn = df[second_knn_columns].values

    query_point_first_knn = X_first_knn[input_song_index]
    input_song_neighbors_first = knn(X_first_knn, query_point_first_knn, k=101)

    query_point_second_knn = X_second_knn[input_song_neighbors_first[0]]
    input_song_neighbors_second = knn(X_second_knn, query_point_second_knn, k=21)

    # Get top 20 from custom KNN
    for i, song_index in enumerate(input_song_neighbors_second):
        song_name = df.iloc[song_index]["song"]
        if song_name not in recommendations:
            recommendations.append(song_name)

    return recommendations[:20]