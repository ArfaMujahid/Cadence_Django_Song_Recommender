from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .recommender import get_recommendations

def index(request):
    return render(request, 'music_recommender/index.html')

@csrf_exempt
@require_http_methods(["POST"])
def recommend(request):
    song_name = request.POST.get('song_name', '').strip()
    artist_name = request.POST.get('artist_name', '').strip()

    if not song_name or not artist_name:
        return JsonResponse({'recommendations': [{'song_name': 'Please provide both song name and artist name'}]})

    try:
        recommendations = get_recommendations(song_name, artist_name)

        if not recommendations:
            return JsonResponse({'recommendations': [{'song_name': 'Song not found in dataset'}]})

        response_data = []
        for song in recommendations:
            response_data.append({'song_name': song})

        return JsonResponse({'recommendations': response_data})

    except Exception as e:
        return JsonResponse({'recommendations': [{'song_name': f'Error occurred: {str(e)}'}]})
