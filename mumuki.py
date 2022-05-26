import requests
import inspect
import sys
from bs4 import BeautifulSoup
from IPython.core.display import display, HTML
from IPython.core.getipython import get_ipython

class BaseMumuki():
    def __init__(self, token:str, locale:str, url = "https://mumuki.io"):
        self.__token = token
        self.__url = url
        self.__locale = locale
        self.__solution = None
        self._register_globals()

    def visit(self, organization:str, exercise):
        self._prepare_before_visit()

        self.__organization = organization
        self.__exercise_id = int(exercise)

        if self._offline():
            return

        try:
            self._connect_after_visit()
        except:
            raise RuntimeError(f"Could not visit exercise {exercise}. Please visit {self.__exercise_url()} and verify the instructions")

    def __solution_url(self):
        return f"{self.__exercise_url()}/solutions"

    def __exercise_url(self):
        return f"{self.__url}/{self.__organization}/exercises/{self.__exercise_id}"

    def __headers(self):
        return { "Authorization": f"Bearer {self.__token}" }

    def _get_exercise(self):
        return requests.get(
             self.__exercise_url(),
             headers = self.__headers())

    def __post_solution(self):
        return requests.post(
            self.__solution_url(),
            json = { "solution": { "content": self.__solution } },
            headers = self.__headers())

    def register_solution(self, function=None):
        self.__solution = self._get_source(function)

    def get_solution(self):
        return self.__solution

    def test(self, function=None):
        self._prepare_before_test()
        if self.__solution is None:
            self.register_solution(function)
        self._submit()

    def _submit(self):
        if self._offline():
            return

        self._report_results(self.__post_solution().json())

    def _get_source(self, function=None):
        if type(function) == str:
            return function
        if function is not None:
            lines = inspect.getsourcelines(function)[0][1:]
            indent_size = inspect.indentsize("".join(line.rstrip("\n\t ") for line in lines))
            return "".join(line[indent_size:] for line in lines)
        else:
            return self._source_missing()


class Mumuki(BaseMumuki):
    def _prepare_before_visit(self):
        frame = inspect.stack()[2]
        self.__start_line = frame.lineno
        self.__file = frame.filename

    def _register_globals(self):
        pass

    def _source_missing(self):
        with open(self.__file) as f:
            return "".join(f.readlines()[self.__start_line:self.__end_line-1])

    def _connect_after_visit(self):
        self._get_exercise()
        print("OK")

    def _prepare_before_test(self):
        frame = inspect.stack()[2]
        self.__end_line = frame.lineno

    def _report_results(self, results):
        print(results['status'])

    def _offline(self):
        return sys.flags.interactive

class IMumuki(BaseMumuki):
    def show(self):
        soup = BeautifulSoup(self._get_exercise().text, "html.parser")
        display(HTML(str(soup.body.find_all("h1")[0])))
        display(HTML(str(soup.body.find_all("div", {"class":"exercise-assignment"})[0])))

    def _register_globals(self):
        def solution(_line, cell):
            self.register_solution(cell)
            get_ipython().run_cell(cell)

        get_ipython().register_magic_function(solution, 'cell', 'solution')

    def _source_missing(self):
        raise RuntimeError("Please ensure to mark you solution cell with %%solution")

    def _prepare_before_visit(self):
        pass

    def _connect_after_visit(self):
        self.show()

    def _prepare_before_test(self):
        pass

    def _report_results(self, results):
        display(HTML(results["html"]))

    def _offline(self):
        return False
