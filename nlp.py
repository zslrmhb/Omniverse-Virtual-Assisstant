# natural language processing module utilizing the Riva SDK 

import wikipedia as wiki
import wikipediaapi as wiki_api
import riva.client
from config import URI


class NLPService:
    def __init__(self, max_wiki_articles):
        """
        :param max_wiki_articles: max wiki articles to search
        """
        self.max_wiki_articles = max_wiki_articles
        self.wiki_summary = " "
        self.input_query = " "
        self.auth = riva.client.Auth(uri=URI)
        self.service = riva.client.NLPService(self.auth)
        self.wiki_wiki = wiki_api.Wikipedia('en')

    def wiki_query(self, input_query) -> None:
        """
        :param input_query: word to search
        :return: None
        """
        self.wiki_summary = " "
        self.input_query = input_query
        wiki_articles = wiki.search(input_query)
        for article in wiki_articles[:min(len(wiki_articles), self.max_wiki_articles)]:
            print(f"Getting summary for: {article}")
            page = self.wiki_wiki.page(article)
            self.wiki_summary += "\n" + page.summary

    def nlp_query(self) -> None:
        """
        :return: Response from the NLP model
        """
        resp = self.service.natural_query(self.input_query, self.wiki_summary)
        if len(resp.results[0].answer) == 0:
            return "Sorry, I don't understand, may you speak again?"
        else:
            return resp.results[0].answer
