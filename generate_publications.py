import bibtexparser


def clean(text):
    if not text:
        return ""
    return text.replace("{", "").replace("}", "").strip()


def format_authors(author_string):

    authors = []

    for author in author_string.split(" and "):

        author = clean(author)

        if "," in author:
            surname, given = [x.strip()
                              for x in author.split(",", 1)]

            initials = " ".join(
                f"{p[0]}."
                for p in given.replace(".", "").split()
                if p
            )

            formatted = f"{surname}, {initials}"

            if surname.lower() == "fluke":
                formatted = f"**{formatted}**"

            authors.append(formatted)

        else:
            authors.append(author)

    return ", ".join(authors)


# ----------------------------------------------------
# Read bibliography
# ----------------------------------------------------

with open("publications.bib",  encoding="utf-8") as bibfile:
    db = bibtexparser.load(bibfile)

entries = db.entries

print(f"Found {len(entries)} entries")

# ----------------------------------------------------
# Sort newest first
# ----------------------------------------------------

entries.sort(
    key=lambda e: int(e.get("year", 0)),
    reverse=True
)

# ----------------------------------------------------
# Generate publications.qmd
# ----------------------------------------------------

current_year = None
count = 1

with open("publications.qmd", "w", encoding="utf-8") as out:

    out.write("---\n")
    out.write("title: Publications\n")
    out.write("---\n\n")

    for entry in entries:

        year = entry.get("year", "Unknown")

        if year != current_year:
            out.write(f"\n\n## {year}\n\n")
            current_year = year

        title = clean(entry.get("title", ""))

        authors = format_authors(
            entry.get("author", "")
        )

        journal = clean(
            entry.get("journal")
            or entry.get("booktitle", "")
        )

        volume = entry.get("volume")
        number = entry.get("number")
        pages  = entry.get("pages")

        out.write(
            f"\n{count}. **{title}**  \n"
        )

        if authors:
            out.write(
                f"   {authors}  "
            )

        if journal:
            out.write(
                f"   *{journal}*  "
            )

        if volume:
            out.write(f"   {volume}  ")

        if number:
            out.write(f"   {number}  ")

        if pages:
            out.write(f"   {pages}  ")

        # ----------------------------------------
        # Links
        # ----------------------------------------

        links = []

        adsurl = clean(
            entry.get("adsurl", "")
        )

        if adsurl:		
            links.append(
                f"[ADS]({adsurl})"
            )
            #links.append(
            #    f"{adsurl}"
            #)

        doi = clean(
            entry.get("doi", "")
        )

        if doi:

            if doi.startswith("http"):
                doi_url = doi
            else:
                doi_url = f"https://doi.org/{doi}"

            links.append(
                f"[DOI]({doi_url})"
            )

        pdfurl = clean(
            entry.get("pdf", "")
        )

        if pdfurl:
            links.append(
                f"{pdfurl}"
            )

        if links:
            out.write(
                "   " + " | ".join(links) + "  "
            )

        out.write("")

        count += 1

print(
    f"Generated publications.qmd with {count-1} entries."
)
