from bs4 import BeautifulSoup
import re
import subprocess
from aops_script import get_items



def get_enum_style(tag):
    try:
        styles = {"lower-roman": "i.", "upper-roman": "I.", "lower-alpha": "a.", "upper-alpha": "A."}
        return "[" + styles[re.search(r"list-style-type\s*:\s*(\S*)", tag["style"]).group(1).strip()] + "]"
    except:
        return ""


def process_latex(problem_html):
    problem_soup = BeautifulSoup(problem_html, "html.parser")

    def span(tag):
        try:
            if "cmty-hide-heading" in tag["class"] and "faux-link" in tag["class"]:
                return tag.get_text() + " \\\\\n"
        except:
            pass
        return(tag.get_text())

    tag_replacements = [
        ["img", lambda tag: process_equation(tag["alt"], tag)],
        ["span", lambda tag: span(tag)],
        ["i", lambda tag: "\\textit{" + tag.get_text() + "}"],
        ["li", lambda tag: "  \\item " + tag.get_text()],
        ["ul", lambda tag: "\\begin{itemize}" + tag.get_text() + "\\end{itemize}"],
        ["ol", lambda tag: "\\begin{enumerate}" + get_enum_style(tag) + tag.get_text() + "\\end{enumerate}"],
        ["b", lambda tag: "\\textbf{" + tag.get_text() + "}"],
        ["a", lambda tag: tag.get_text()],
        ["hr", lambda tag: "\\rule{\linewidth}{0.5mm}"]
    ]
    for tag in tag_replacements:
        for i in problem_soup.find_all(tag[0]):
            i.replaceWith(tag[1](i))
    latex = str(problem_soup)

    regex_replacements = [
        [r"(?:<br\/?>|\s)*\\\[", "\n\["],
        [r"\\\](?:<br\/?>|\s)*", "\]\n"],
        [r"(?<=[^\\])&amp;", r"\&"],
        [r"\&amp;", r"&"],
        [r"\"([a-zA-Z0-9])", r"``\1"],
        [r"(?:\s|<br\s*\/?>)*(\\begin{[^}]*})", r"\n\1"],
        [r"(\\end{[^}]*})(?:\s|<br\s*\/?>)*", r"\1\n"],
        [r"\s*<br\/?>(?:<br\/?>|\s)*", lambda text: " " + "\\\\"*(len(text.group(0).split("<br")) - 1) + "\n"],
        [r"\\\]\W*\.", r".\\]"],
    ]
    for i in regex_replacements:
        latex = re.sub(i[0], i[1], latex)

    replacements = [
        ["&lt;", "<"],
        ["&gt;", ">"],
        ["&ge;", "\\ge"],
        ["&gte;", "\\ge"],
        ["&le;", "\\le"],
        ["&lte;", "\\le"],
        ["&nbsp;", ""],
        ["−", "-"]
    ]
    for i in replacements:
        latex = latex.replace(i[0], i[1])

    lines = (latex + "\n").split("\n")
    for i in range(len(lines)):
        if re.match(r"(?i)\(?(?:i*v?|[abcdef123456])[\.\)]", lines[i].strip()):
            lines[i] = [lines[i], True, re.sub(r"(?i)\(?(?:i*v?|[abcdef123456])[\.\)]", r"", lines[i].strip(), 1).strip("\\").strip()]
        else:
            lines[i] = [lines[i], False, None]

    output = ""
    enumsection = [False, False]
    for i in lines:
        if not i[1] and enumsection[0]:
            if enumsection[1]:
                output += "\\end{enumerate}\n"
            enumsection = [False, False]
        if i[1] and not enumsection[0]:
            match = re.match(r"\(?[iIaA1][\.\)]", i[0].strip())
            if match is not None:
                output += "\\begin{enumerate}" + ("[" + match.group(0) + "]" if match.group(0) != "1." else "") + "\n"
            enumsection = [True, match is not None]
        if i[1] and enumsection[1]:
            output += "  \\item " + i[2] + "\n"
        else:
            output += i[0] + "\n"

    output = re.sub(r"[\\\s]*\\begin{enumerate}", r"\n\\begin{enumerate}", output)
    output = re.sub(r"\\end{enumerate}[\\\s]*\s", r"\\end{enumerate}\n", output)

    return(output.strip())




def process_equation(latex, tag):
    if latex.strip().startswith("[asy]"):
        return("\\begin{center}\n\\begin{asy}[width=" + str(int(0.6*int(tag["width"]))) + "pt]\nsize(" + str(int(0.6*int(tag["width"]))) + ", " + str(int(0.6*int(tag["height"]))) + ");\n" + latex.strip()[5:-6].strip().replace("\"", "'") + "\n\\end{asy}\n\\end{center}")

    latex = latex.strip()
    if latex.startswith("$$"):
        latex = "\[" + latex[2:-2].strip() + "\]"

    regex_replacements = [
        [r"_\{(.)\}", r"_\1"],
        [r"\^\{(.)\}", r"^\1"],
        [r"\\\[\s*", r"\[ "],
        [r"\s*\\\]", r" \]"]
    ]
    for i in regex_replacements:
        latex = re.sub(i[0], i[1], latex)

    replacements = [
        ["\]", "\]\n"],
        ["&amp;", "\&"]
    ]
    for i in replacements:
        latex = latex.replace(i[0], i[1])

    if latex.startswith("\[") and len(latex) > 100:
        latex = latex.replace("\[ ", "\[\n").replace(" \]", "\n\]")

    return(latex)




def process_item(item, render=True):
    latex = process_latex(str(item["post_data"]["post_rendered"]))

    return(latex)
