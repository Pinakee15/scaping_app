from abc import ABC, abstractmethod

class NotifierInterface(ABC):
    @abstractmethod
    def notify(self, scraped: int, updated: int):
        pass

class ConsoleNotifier(NotifierInterface):
    def notify(self, scraped: int, updated: int):
        print(f"Scraping completed. Products scraped: {scraped}, Products updated: {updated}")

