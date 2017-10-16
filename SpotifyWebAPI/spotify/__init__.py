# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.


from bases import (
    AudioFeature,
    Artist,
    Album,
    Playlist,
    Recommendations,
    SavedAlbum,
    Track,
    User,
    PlayHistory,
)


class Albums(object):
    def get_albums(self, ids):
        '''
        GET 	/v1/albums/{id}        SINGLE ALBUM
        GET 	/v1/albums?ids={ids}
        '''

    def add_albums(self, albums):
        '''
        PUT 	/v1/me/albums?ids={ids}
        '''

    def saved_albums(self):
        '''
        GET 	/v1/me/albums
        '''

    def delete_albums(self):
        '''
        DELETE	/v1/me/albums?ids={ids}
        '''

    def is_album_saved(self, album):
        '''
        GET 	/v1/me/albums/contains?ids={ids}
        '''


class Playlists(object):
    '''
    GET 	/v1/me/playlists
    GET 	/v1/users/{user_id}/playlists/{playlist_id}
    GET 	/v1/users/{user_id}/playlists/{playlist_id}/tracks
    POST	/v1/users/{user_id}/playlists
    PUT 	/v1/users/{user_id}/playlists/{playlist_id}
    POST	/v1/users/{user_id}/playlists/{playlist_id}/tracks
    DELETE	/v1/users/{user_id}/playlists/{playlist_id}/tracks
    PUT 	/v1/users/{user_id}/playlists/{playlist_id}/tracks
    PUT 	/v1/users/{user_id}/playlists/{playlist_id}/tracks
    GET 	/v1/users/{user_id}/playlists/{playlist_id}/followers/contains
    PUT 	/v1/users/{user_id}/playlists/{playlist_id}/images

    PUT 	/v1/users/{owner_id}/playlists/{playlist_id}/followers
    DELETE 	/v1/users/{owner_id}/playlists/{playlist_id}/followers
    GET 	/v1/users/{user_id}/playlists
    '''


class Tracks(object):
    '''
    PUT     /v1/me/tracks?ids={ids}
	GET     /v1/me/tracks
	DELETE	/v1/me/tracks?ids={ids}
    GET 	/v1/me/tracks/contains?ids={ids}

    GET 	/v1/tracks/{id}
    GET 	/v1/tracks?ids={ids}
    '''


class Artists(object):
    '''
    GET 	/v1/artists/{id}
	GET 	/v1/artists?ids={ids}
    GET 	/v1/artists/{id}/albums
    GET 	/v1/artists/{id}/top-tracks
    GET 	/v1/artists/{id}/related-artists
    '''


class Player(object):
    '''
    GET 	v1/me/player/recently-played
    GET 	/v1/me/player/devices
    GET 	/v1/me/player
    GET 	/v1/me/player/currently-playing
    PUT 	/v1/me/player
    PUT 	/v1/me/player/play
    PUT 	/v1/me/player/pause
    POST	/v1/me/player/next
    POST	/v1/me/player/previous
    PUT 	v1/me/player/seek
    PUT 	/v1/me/player/repeat
    PUT 	/v1/me/player/volume
    PUT 	/v1/me/player/shuffle
    '''


class Audio(object):
    '''
    GET 	v1/audio-analysis/{id}
    GET 	/v1/audio-features/{id}
    GET 	/v1/audio-features?ids={ids}
    '''


class Search(object):
    '''
    GET 	/v1/search?type=album
    GET 	/v1/search?type=artist
	GET 	/v1/search?type=playlist
    GET 	/v1/search?type=track
    '''


class SpotifyHandler(object):
    '''



    GET 	/v1/browse/featured-playlists
    GET 	/v1/browse/new-releases
    GET 	/v1/browse/categories
    GET 	/v1/browse/categories/{id}
    GET 	/v1/browse/categories/{id}/playlists
    GET 	/v1/me
    GET 	/v1/me/following
    PUT 	/v1/me/following
    DELETE	/v1/me/following
    GET 	/v1/me/following/contains



	GET 	/v1/me/top/{type}
    GET 	/v1/recommendations







* Simplified objects
Authorization

Endpoints marked “OAuth” above require application registration and user authorization via the Spotify Accounts Service to access certain data.

Accounts Service Base URL: https://accounts.spotify.com       Authorization Guide | Using Scopes | Tutorial
Method
	Endpoint
	Usage
GET
	/authorize
	Get an authorization code
POST
	/api/token
	Get an access token (or an access token and refresh token)

Note that all endpoints benefit from increased rate limits when a valid access token is passed in the call.
API Specification

We have made available a specification of our API using RAML that you can find on the Web API GitHub repo.

RAML is a YAML-based language that describes RESTful APIs and provides all the information necessary to describe RESTful APIs, create API client-code and API server-code generators, and create API user documentation from RAML API definitions.

    '''

    @property
    def user_profile(self):
        '''
        GET 	/v1/users/{user_id}
        '''

    def __init__(self):
        pass



