# albums/views.py
import json

from django.shortcuts import render, redirect
from .forms import ArrayForm
from pymongo import MongoClient
from django.conf import settings
from pymongo.errors import ConnectionFailure

def insert_array(request):
    if request.method == 'POST':
        form = ArrayForm(request.POST)
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
                form.add_error(None, f'{count} Albums inserted successfully.')
                # return redirect('success_url')  # Redirect to a new URL for success
            except ConnectionFailure:
                form.add_error(None, 'Database connection failed. Please try again later.')
    else:
        form = ArrayForm()

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
        'albums_queued' : albums_count
    }
    return render(request, 'albums/insert_albums.html', context)
