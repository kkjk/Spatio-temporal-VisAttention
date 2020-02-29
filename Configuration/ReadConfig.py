import json
import os



class ParseJson:
    """
    This class reads the configuration file and parses it according to the services offered.
    This is later used by the orchestrator to send the config info to the corresponding services

    """

    def __init__(self, filePath):
        """
        Constructor of the class

        """
        self.jsonFileName = filePath
        self.parsedData = self.parseJson()

    def parseJson(self):
        """
        json parser

        """
        with open(self.jsonFileName) as f_in:
            return json.load(f_in)

    def getStaticConfig(self):
        """
        static prediciton configuration

        """
        return self.parsedData["Static"]

    def getDynamicConfig(self):
        """
        dynamic prediciton configuration

        """
        return self.parsedData["Dynamic"]

    def getLstmStaticConfig(self):
        """
        LSTM static prediciton configuration

        """
        return self.parsedData["Lstm_Static"]

    def getLstmDynamicConfig(self):
        """
        LSTM dynamic prediciton configuration

        """
        return self.parsedData["Lstm_Dynamic"]

