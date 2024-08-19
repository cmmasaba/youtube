# views.py
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from pytube import YouTube, Playlist
import os
import tempfile

def index(request):
    return render(request, 'index.html')

def download_video(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        format = request.POST.get('format')
        quality = request.POST.get('quality')
        download_type = request.POST.get('download_type')

        try:
            if download_type == 'playlist':
                playlist = Playlist(url)
                temp_dir = tempfile.mkdtemp()

                for video in playlist.videos:
                    stream = video.streams.filter(file_extension=format, res=quality).first()
                    stream.download(output_path=temp_dir)

                zip_filename = os.path.join(temp_dir, "playlist.zip")
                os.system(f'zip -r {zip_filename} {temp_dir}')
                response = HttpResponse(open(zip_filename, 'rb'), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename="playlist.zip"'
                os.remove(zip_filename)
                return response
            else:
                yt = YouTube(url)
                stream = yt.streams.filter(file_extension=format, res=quality).first()
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{format}")
                stream.download(filename=temp_file.name)
                response = HttpResponse(open(temp_file.name, 'rb'), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{yt.title}.{format}"'
                os.remove(temp_file.name)
                return response
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)
