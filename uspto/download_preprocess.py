from typing import Literal

import lxml.html as html
import requests


def convert_mathml_to_latex(url: str, mathml_string: str) -> str:
    """Function to convert MathML to LaTeX using a REST server running https://github.com/asnunes/mathml-to-latex."""
    if not mathml_string:
        return ""
    response = requests.post(url, json={"mathml": mathml_string})
    if response.status_code in [400, 500]:
        return str(mathml_string)
    else:
        result = response.json()
        return result.get("latex", mathml_string)


def parse_html(url, html_string: str) -> str:
    html_string = html.fromstring(html_string)
    equations: list[html.HtmlElement] = html_string.xpath("//maths")
    if equations:
        for i, eq in enumerate(equations):
            new_equation = convert_mathml_to_latex(url, str(eq))
            eq.clear()
            eq.text = new_equation
    return html_string.text_content()