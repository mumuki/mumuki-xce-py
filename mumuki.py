import requests
import inspect
import sys
from bs4 import BeautifulSoup
from IPython.core.display import display, HTML

class Mumuki():
    def __init__(self, token, url = "https://mumuki.io"):
        self.__token = token
        self.__url = url

    def visit(self, organization, exercise, show=True):
        if type(exercise) == int:
            self.__organization = organization
            self.__exercise_id = exercise
        else:
            raise RuntimeError(f"Unknown exercise {exercise}")

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

    def __post_solution(self, solution):
        return requests.post(
            self.__solution_url(),
            json = { "solution": { "content": solution } },
            headers = self.__headers())

    def show(self):
        soup = BeautifulSoup(self.__get_exercise().text, "html.parser")
        display(HTML(str(soup.body.find_all("h1")[0])))
        display(HTML(str(soup.body.find_all("div", {"class":"exercise-assignment"})[0])))

    def submit(self, solution):
        display(HTML(self.__post_solution(solution).json()["html"]))

    def get_main_solution(self):
        return getattr(sys.modules['__main__'], 'solution')

    def test(self, function=None):
        self.submit(self.get_source(function))

    def get_source(self, function=None):
        solution = function or self.get_main_solution()
        lines = inspect.getsourcelines(solution)[0][1:]
        indent_size = inspect.indentsize("".join(line.rstrip("\n\t ") for line in lines))
        return "".join(line[4:] for line in lines)