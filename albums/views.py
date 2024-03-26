# albums/views.py
import json

from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import AlbumDataForm
from pymongo import MongoClient
from django.conf import settings
from pymongo.errors import ConnectionFailure
import os
def get_albums(skip=0, limit=25):
    albums = []
    try:
        client = MongoClient(settings.MONGO_URI)
        db = client[settings.MONGO_DATABASE_NAME]
        collection = db['_queue_up_albums']
        latest_albums = collection.find().sort([('_id', 1)]).skip(skip).limit(limit)
        for album in latest_albums:
            if album['album']['cover'] is not None:
                album['image'] = (os.environ.get('image_static_resource') +
                                  album['album']['cover'].replace('-', '/')) + '/80x80.jpg'
            else:
                album['image'] = os.environ.get('image_static_local') + '/old-record.webp'
            albums.append(album)
        client.close()
        return albums
    except ConnectionFailure:
        return albums

def insert_array(request):
    if request.method == 'POST':
        form = AlbumDataForm(request.POST)
        if form.is_valid():
            array_data = form.cleaned_data['array_data']
            try:
                # deserialize the json string to object
                new_array = json.loads(array_data)
                # verifiy the new_array is a list
                if not isinstance(new_array, list):
                    form.add_error(None, 'The input was not a list.')
                    return render(request, 'albums/insert_albums.html', {'form': form})
                client = MongoClient(settings.MONGO_URI)
                db = client[settings.MONGO_DATABASE_NAME]
                collection_unknown = db['_queue_up_unknown_data']
                collection_queue = db['_queue_up_albums']
                collection_known = db['known_albums']
                count_queue_inserts = 0
                for item in new_array:
                    if item['numberOfTracks'] is None:
                        # this is not an album 
                        collection_unknown.insert_one({"unknown": item, "orgin": "albums"})
                        continue
                    # check known albums first for id ..
                    does_exist = collection_known.find_one({"album.id": item['id']})
                    if does_exist :
                        continue
                    # check queue ...
                    does_exist = collection_queue.find_one({"album.id": item['id']})
                    if does_exist is None:
                        collection_queue.insert_one({"album": item})
                        count_queue_inserts += 1
                # TODO: Why is this even split? / this logic can be moved into the top loop
                count_known_inserts = 0
                for item in new_array:
                    if item['numberOfTracks'] is None:
                        # this is not an album
                        continue
                    does_exist = collection_known.find_one({"album.id": item['id']})
                    if does_exist is None:
                        collection_known.insert_one({"album": item, "tracks_known": False, "related_known" : False})
                        count_known_inserts += 1 # if the known album is checked first this number wont matter anymore
                client.close()
                messages.success(request, f'{count_queue_inserts} Albums inserted successfully.')
                # return redirect('success_url')  # Redirect to a new URL for success
            except ConnectionFailure:
                messages.error(request, 'Database connection failed. Please try again later.')
    else:
        form = AlbumDataForm()

    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DATABASE_NAME]
    collection_known = db['known_albums']
    collection_albums = db['_queue_up_albums']
    # Count all documents in each collection
    known_count = collection_known.count_documents({})
    albums_count = collection_albums.count_documents({})
    context = {
        'form': form,
        'albums_known' : known_count,
        'albums_queued' : albums_count,
        'albums': get_albums(0,25),
        'next_up': get_albums(25,25)
    }
    return render(request, 'albums/insert_albums.html', context)
