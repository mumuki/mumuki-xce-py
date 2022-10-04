from bs4 import BeautifulSoup
from IPython.core.display import display, HTML
from IPython.core.getipython import get_ipython

from mumuki.base import BaseMumuki

class IMumuki(BaseMumuki):
    def show(self):
        soup = self._make_soup(self._get_exercise().text)
        display(self._to_html(soup.body.find_all("h1")[0]))
        display(self._to_html(soup.body.find_all("div", {"class":"exercise-assignment"})[0]))

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
        display(self._to_html(self._make_soup(results["html"])))

    def _offline(self):
        return False

    def _make_soup(self, html):
        soup = BeautifulSoup(html, "html.parser")
        for link in soup.find_all("a"):
            link['target'] = '_blank'
        return soup

    def _to_html(self, soup):
        return HTML(str(soup))
