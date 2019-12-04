from __future__ import print_function
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request



class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted =models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk' : self.pk})


class Calendar():

# If modifying these scopes, delete the file token.pickle.
	SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

	def getCalendarData(self):
	    """Shows basic usage of the Google Calendar API.
	    Prints the start and name of the next 10 events on the user's calendar.
	    """
	    creds = None
	    # The file token.pickle stores the user's access and refresh tokens, and is
	    # created automatically when the authorization flow completes for the first
	    # time.
	    if os.path.exists('token.pickle'):
	        with open('token.pickle', 'rb') as token:
	            creds = pickle.load(token)
	    # If there are no (valid) credentials available, let the user log in.
	    if not creds or not creds.valid:
	        if creds and creds.expired and creds.refresh_token:
	            creds.refresh(Request())
	        else:
	            flow = InstalledAppFlow.from_client_secrets_file(
	                'credentials.json', self.SCOPES)
	            creds = flow.run_local_server(port=0)
	        # Save the credentials for the next run
	        with open('token.pickle', 'wb') as token:
	            pickle.dump(creds, token)

	    service = build('calendar', 'v3', credentials=creds)

	    # Call the Calendar API
	    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	    print('Getting the upcoming 10 events')
	    events_result = service.events().list(calendarId='primary', timeMin=now,
	                                        maxResults=10, singleEvents=True,
	                                        orderBy='startTime').execute()
	    events = events_result.get('items', [])
	    data = []
	    if not events:
	    	data += 'No event found.'
	        #print('No upcoming events found.')
	    for event in events:
	        start = event['start'].get('dateTime', event['start'].get('date'))
	        data.append(event['summary'])
	        #print(start, event['summary'])
	    return data