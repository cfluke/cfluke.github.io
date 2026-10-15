#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 4096
#define MAX_FIELD 8192

typedef struct {
    char title[MAX_FIELD];
    char author[MAX_FIELD];
    char journal[MAX_FIELD];
    char year[32];
    char doi[MAX_FIELD];
    char adsurl[MAX_FIELD];
    char pdf[MAX_FIELD];
} Entry;

static void trim(char *s)
{
    char *p;

    while (*s == ' ' || *s == '\t')
        memmove(s, s + 1, strlen(s));

    p = s + strlen(s) - 1;

    while (p >= s &&
           (*p == '\n' || *p == '\r' ||
            *p == ',' ||
            *p == ' '))
    {
        *p = '\0';
        p--;
    }
}

static void extract_value(char *dest, const char *line)
{
    const char *start;
    const char *end;

    dest[0] = '\0';

    start = strchr(line, '{');

    if (!start)
        return;

    start++;

    end = strrchr(start, '}');

    if (!end)
        return;

    strncpy(dest, start, end - start);
    dest[end - start] = '\0';
}

int main(void)
{
    FILE *in;
    FILE *out;

    char line[MAX_LINE];

    Entry entry;

    int current_year = -1;

    in = fopen("publications.bib", "r");

    if (!in)
    {
        perror("publications.bib");
        return 1;
    }

    out = fopen("publications.qmd", "w");

    if (!out)
    {
        perror("publications.qmd");
        return 1;
    }

    fprintf(out,
        "---\n"
        "title: Publications\n"
        "---\n\n");

    fprintf(out, "<ol>\n");

    memset(&entry, 0, sizeof(entry));

    while (fgets(line, sizeof(line), in))
    {
        if (strncmp(line, "@", 1) == 0)
        {
            memset(&entry, 0, sizeof(entry));
            continue;
        }

        if (strstr(line, "title"))
            extract_value(entry.title, line);

        else if (strstr(line, "author"))
            extract_value(entry.author, line);

        else if (strstr(line, "journal"))
            extract_value(entry.journal, line);

        else if (strstr(line, "year"))
            extract_value(entry.year, line);

        else if (strstr(line, "doi")) 
            extract_value(entry.doi, line);

        else if (strstr(line, "adsurl"))
            extract_value(entry.adsurl, line);

        else if (strstr(line, "pdf"))
            extract_value(entry.pdf, line);

        else if (strchr(line, '}'))
        {
            int y = atoi(entry.year);

            if (y != current_year)
            {
                fprintf(out,
                    "</ol>\n\n"
                    "## %d\n\n"
                    "<ol>\n",
                    y);

                current_year = y;
            }

            fprintf(out, "<li>\n");

            fprintf(out,
                "<strong>%s</strong><br>\n",
                entry.title);

            fprintf(out,
                "%s<br>\n",
                entry.author);

            fprintf(out,
                "<em>%s</em><br>\n",
                entry.journal);

            int first = 1;

            if (strlen(entry.adsurl))
            {
                fprintf(out,
                    "\"%s\"ADS</a>",
                    entry.adsurl);
                first = 0;
            }

            if (strlen(entry.doi))
            {
	        fprintf(stderr,"DOI: %s\n",entry.doi);
                if (!first)
                    fprintf(out, "<a href=");

                fprintf(out,
                    "\"https://doi.org/%s\">DOI</a>",
                    entry.doi);

                first = 0;
            }

            if (strlen(entry.pdf))
            {
                if (!first)
                    fprintf(out, " | ");

                fprintf(out,
                    "\"%s\"PDF</a>",
                    entry.pdf);
            }

            fprintf(out, "\n</li>\n\n");
        }
    }

    fprintf(out, "</ol>\n");

    fclose(in);
    fclose(out);

    printf("Generated publications.qmd\n");

    return 0;
}
