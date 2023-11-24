import json
import requests

class ScienceDayAPI:
    def __init__(self, url: str) -> None:
        self.url = url
        self.participants = self.getParticipants()

    def getParticipants(self) -> dict:
        """Returns a dictionary with the id of the participants as keys for all participants
        """
        dataApi = json.loads(requests.get(self.url).text)

        results = {}
        for instance in dataApi:
            results[instance['id']] = {'player_alias':instance['player_alias'], 'player_score':instance['player_score'], 'player_time':instance['player_time']}

        return results
    
    def getNewParticipants(self) -> dict:
        """Returns all participants that were added to the API
        """
        updatedParticipants = self.getParticipants()

        s = set(self.participants.keys())
        difference = [x for x in updatedParticipants if x not in s]

        results = {}
        for id in difference:
            results[id] = updatedParticipants[id]

        return results
    
    def updateParticipants(self) -> None:
        self.participants = self.getParticipants()