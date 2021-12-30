# Description
Mining Massive Datasets Project. A recommendation system built with Spotify’s API with a database created using Billboards top 100 artists per year. When script is ran the user inputs a Spotify song link and then the a playlist is created on their account with 10 recommended songs.

# Database

| id                     | energy | liveness | tempo   | speechiness | acousticness | instrumentalness | time_signature | danceability | key | duration_ms | loudness | valence | name                   |
| ---------------------- | ------ | -------- | ------- | ----------- | ------------ | ---------------- | -------------- | ------------ | --- | ----------- | -------- | ------- | ---------------------- |
| 7sWRlDoTDX8geTR8zzr2vt | 0.646  | 0.103    | 130.218 | 0.0476      | 0.331        | 0                | 4              | 0.405        | 4   | 156267      | -3.206   | 0.17    | Hollywood's Bleeding   |
| 05mDaV9Vb3wrzjF6OPZnhq | 0.684  | 0.104    | 132.113 | 0.0439      | 0.0545       | 0                | 4              | 0.617        | 0   | 150867      | -3.618   | 0.295   | Saint-Tropez           |
| 0Xek5rqai2jcOWCYWJfVCF | 0.674  | 0.0955   | 76.388  | 0.21        | 0.0588       | 0                | 4              | 0.542        | 6   | 196760      | -4.169   | 0.667   | Enemies (feat. DaBaby) |
| 1YscJ7yVTlFxW3eF6pv5ba | 0.741  | 0.345    | 144.968 | 0.0787      | 0.154        | 3.02E-05         | 4              | 0.665        | 0   | 156893      | -3.694   | 0.57    | Allergic               |
| 2J0NXdHr6MYvKDSxB7k3V2 | 0.732  | 0.111    | 159     | 0.092       | 0.105        | 1.15E-05         | 4              | 0.632        | 6   | 221173      | -3.498   | 0.317   | A Thousand Bad Times   |
| 21jGcNKet2qwijlDFuPiPb | 0.762  | 0.0863   | 120.042 | 0.0395      | 0.192        | 0.00244          | 4              | 0.695        | 0   | 215280      | -3.497   | 0.553   | Circles                |

Songs are composed many audio features these were the ones gathered:
- **energy**: Measure of intensity and activity.
- **liveness**: Detects the presence of an audience in the recording. 
- **tempo**: The overall estimated tempo of a track in beats per minute (BPM).
- **speechiness**: Detects the presence of spoken words in a track. 
- **acousticness**: A confidence measure of whether the track is acoustic.
- **instrumentalness**: Predicts whether a track contains no vocals.
- **time_signature**: Estimated time signature. 
- **danceability**: Describes how suitable a track is for dancing based on a combination of musical elements.
- **duration_ms**: The duration of the track in milliseconds.
- **loudness**: The overall loudness of a track in decibels (dB). 
- **valence**: The musical positiveness conveyed by a track. 
