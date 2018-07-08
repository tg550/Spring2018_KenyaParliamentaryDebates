Construct a JSON file containing meta-data for each txt file in the Box folder.
--------

For each of the OCR'd txt files in the Outputs folder on Box, we need to know two important pieces of metadata: the line number on which the verbatim transcripts start and the line number on which the verbatim transcripts end. 

Many of the txt files are structured like a book, where the first few hundred lines in the file consist of front-matter (table of contents, preamble, et cetera); then there are the verbatim transcripts of one or more sittings of parliament; then it closes with an index and other end-matter. We want to know the line number on which the verbatim transcripts start and the line number on which the verbatim transcripts end.

Having this information makes parsing the transcripts easier, since we can easily ignore the front-matter and end-matter.

