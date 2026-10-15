from bibtexparser import parse_file

library = parse_file("publications.bib")

entry = library.entries[0]

print(type(entry))
print(entry)
