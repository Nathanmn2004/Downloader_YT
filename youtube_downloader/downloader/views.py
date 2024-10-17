from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import yt_dlp
import os
from .forms import DownloadForm

def index(request):
    if request.method == "POST":
        form = DownloadForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            filename = download_audio(url)  # Chame a função de download
            
            if filename and os.path.exists(filename):
                with open(filename, 'rb') as audio_file:
                    response = HttpResponse(audio_file.read(), content_type='audio/mpeg')
                    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(filename)}"'
                    return response
            else:
                return JsonResponse({'error': 'Falha no download'}, status=500)
    else:
        form = DownloadForm()
    return render(request, 'index.html', {'form': form})

def download_audio(url):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
            ydl.download([url])
            return f"downloads/{info['title']}.mp3"
    except Exception as e:
        print(e)
        return None
