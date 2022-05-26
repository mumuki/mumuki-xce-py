import requests
import inspect

class BaseMumuki():
    def __init__(self, token:str, locale:str, url = "https://mumuki.io"):
        self._token = token
        self._url = url
        self._locale = locale
        self._solution = None
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
        return f"{self._url}/{self.__organization}/exercises/{self.__exercise_id}"

    def __headers(self):
        return { "Authorization": f"Bearer {self._token}" }

    def _get_exercise(self):
        return requests.get(
             self.__exercise_url(),
             headers = self.__headers())

    def __post_solution(self):
        return requests.post(
            self.__solution_url(),
            json = { "solution": { "content": self._solution } },
            headers = self.__headers())

    def register_solution(self, function=None):
        self._solution = self._get_source(function)

    def get_solution(self):
        return self._solution

    def test(self, function=None):
        self._prepare_before_test()
        if self._solution is None:
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
