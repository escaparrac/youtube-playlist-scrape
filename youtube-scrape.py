import csv
from googleapiclient.discovery import build

# Tu clave de API de Google Cloud Platform
api_key = 'API KEY HERE'
youtube = build('youtube', 'v3', developerKey=api_key)

# ID de la lista de reproducción de YouTube
playlist_id = 'PLAYLIST ID HERE'

# Función para obtener los metadatos de la lista de reproducción
def get_playlist_items(youtube, playlist_id):
    request = youtube.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()

    # Lista para almacenar los metadatos
    playlist_items = []
    
    while request is not None:
        for item in response['items']:
            # Obtener detalles del video
            video_id = item['contentDetails']['videoId']
            video_request = youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=video_id
            )
            video_response = video_request.execute()
            video_details = video_response['items'][0]

            # Extraer los metadatos requeridos
            title = video_details['snippet']['title']
            description = video_details['snippet']['description']
            thumbnail_url = video_details['snippet']['thumbnails']['default']['url']
            hd_thumbnail_url = video_details['snippet']['thumbnails']['high']['url']
            video_added_to_playlist_at = item['snippet']['publishedAt']
            video_published_at = video_details['snippet']['publishedAt']
            playlist_hosted_channel_name = item['snippet']['channelTitle']
            video_owner_title = video_details['snippet']['channelTitle']
            video_owner_channel_id = video_details['snippet']['channelId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            video_tags = ','.join(video_details['snippet'].get('tags', []))
            category_id = video_details['snippet']['categoryId']
            default_audio_language = video_details['snippet'].get('defaultAudioLanguage', '')
            view_count = video_details['statistics']['viewCount']
            like_count = video_details['statistics']['likeCount']
            favorite_count = video_details['statistics']['favoriteCount']
            video_comment_count = video_details['statistics']['commentCount']
            video_duration = video_details['contentDetails']['duration']

            # Añadir los metadatos a la lista
            playlist_items.append([
                title, description, thumbnail_url, hd_thumbnail_url,
                video_added_to_playlist_at, video_published_at,
                playlist_hosted_channel_name, video_owner_title,
                video_owner_channel_id, video_id, video_url, video_tags,
                category_id, default_audio_language, view_count, like_count,
                favorite_count, video_comment_count, video_duration
            ])
        
        # Verificar si hay más páginas
        if 'nextPageToken' in response:
            request = youtube.playlistItems().list_next(
                previous_request=request,
                previous_response=response
            )
            response = request.execute()
        else:
            request = None
    
    return playlist_items

# Obtener los metadatos de la lista de reproducción
playlist_items = get_playlist_items(youtube, playlist_id)

# Guardar los metadatos en un archivo CSV
with open('playlist_metadata.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow([
        'Título', 'Descripción', 'URL de Miniatura', 'URL de Miniatura HD',
        'Añadido a la Lista de Reproducción', 'Publicado en YouTube',
        'Nombre del Canal de la Lista', 'Título del Propietario del Video',
        'ID del Canal del Propietario del Video', 'ID del Video', 'URL del Video',
        'Etiquetas del Video', 'ID de Categoría', 'Idioma de Audio Predeterminado',
        'Conteo de Vistas', 'Conteo de Me Gusta', 'Conteo de Favoritos',
        'Conteo de Comentarios del Video', 'Duración del Video'
    ])  # Encabezados de las columnas
    writer.writerows(playlist_items)

print('Los metadatos se han guardado en "playlist_metadata.csv"')
