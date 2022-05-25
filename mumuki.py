import requests
import inspect
import sys
from bs4 import BeautifulSoup
from IPython.core.display import display, HTML

class Mumuki():
    def __init__(self, token:str, locale:str, url = "https://mumuki.io"):
        self.__token = token
        self.__url = url
        self.__locale = locale
        self.__solution = None

    def visit(self, organization:str, exercise, show=True):
        self.__organization = organization
        self.__exercise_id = int(exercise)

        try:
            if show:
                self.show()
            else:
                self.__get_exercise()
                print("OK")
        except:
            raise RuntimeError(f"Could not visit exercise {exercise}. Please visit {self.__exercise_url()} and verify the instructions")

    def __solution_url(self):
        return f"{self.__exercise_url()}/solutions"

    def __exercise_url(self):
        return f"{self.__url}/{self.__organization}/exercises/{self.__exercise_id}"

    def __headers(self):
        return { "Authorization": f"Bearer {self.__token}" }

    def __get_exercise(self):
        return requests.get(
             self.__exercise_url(),
             headers = self.__headers())

    def __post_solution(self):
        return requests.post(
            self.__solution_url(),
            json = { "solution": { "content": self.__solution } },
            headers = self.__headers())

    def show(self):
        soup = BeautifulSoup(self.__get_exercise().text, "html.parser")
        display(HTML(str(soup.body.find_all("h1")[0])))
        display(HTML(str(soup.body.find_all("div", {"class":"exercise-assignment"})[0])))

    def register_solution(self, function=None):
        self.__solution = self._get_source(function)

    def get_solution(self):
        return self.__solution

    def test(self, function=None):
        if self.__solution is None:
            self.register_solution(function)
        self._submit()

    def _submit(self):
        display(HTML(self.__post_solution().json()["html"]))

    def _get_main_solution(self):
        return getattr(sys.modules['__main__'], 'solution')

    def _get_source(self, function=None):
        if type(function) == str:
            return function

        solution = function or self._get_main_solution()
        lines = inspect.getsourcelines(solution)[0][1:]
        indent_size = inspect.indentsize("".join(line.rstrip("\n\t ") for line in lines))
        return "".join(line[4:] for line in lines)