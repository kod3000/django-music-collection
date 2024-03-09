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
            album['image'] = (os.environ.get('image_static_resource') +
                              album['album']['cover'].replace('-', '/')) + '/80x80.jpg'
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
                # Insert into MongoDB
                client = MongoClient(settings.MONGO_URI)
                db = client[settings.MONGO_DATABASE_NAME]
                collection_unknown = db['_queue_up_unknown_data']
                collection = db['_queue_up_albums']
                count = 0
                for item in new_array:
                    if item['numberOfTracks'] is None:
                        # this is not an album
                        collection_unknown.insert_one({"unknown": item, "orgin": "albums"})
                        continue
                    does_exist = collection.find_one({"album.id": item['id']})
                    if does_exist is None:
                        collection.insert_one({"album": item})
                        count += 1
                collection = db['known_albums']
                for item in new_array:
                    if item['numberOfTracks'] is None:
                        # this is not an album
                        continue
                    does_exist = collection.find_one({"album.id": item['id']})
                    if does_exist is None:
                        collection.insert_one({"album": item})
                client.close()
                messages.success(request, f'{count} Albums inserted successfully.')
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
