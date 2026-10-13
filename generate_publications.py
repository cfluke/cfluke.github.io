from collections import defaultdict
from bibtexparser import parse_file

library = parse_file("publications.bib")

groups = defaultdict(list)

for entry in library.entries:

    data = entry.fields_dict

    keywords = data.get("keywords")

    if keywords:
        values = keywords.value.split(",")
    else:
        values = ["other"]

    for keyword in values:
        groups[keyword.strip()].append(data)

with open("publications.qmd", "w") as out:

    out.write("---\n")
    out.write("title: Publications\n")
    out.write("---\n\n")

    out.write("# Publications\n\n")

    for keyword in sorted(groups):

        out.write(f"## {keyword.title()}\n\n")

        for paper in sorted(
            groups[keyword],
            key=lambda x: x.get("year", "").value if "year" in x else "",
            reverse=True
        ):

            author = paper.get("author")
            title = paper.get("title")
            journal = paper.get("journal")
            year = paper.get("year")

            author = author.value if author else ""
            title = title.value if title else ""
            journal = journal.value if journal else ""
            year = year.value if year else ""

            out.write(
                f"- {author} ({year}). "
                f"*{title}*. {journal}.\n"
            )

        out.write("\n")
