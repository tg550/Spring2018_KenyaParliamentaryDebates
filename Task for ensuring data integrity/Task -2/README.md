Construct a hand-labeled training set of "line labels".
--------

Before getting to topic modelling, we first need to parse the raw unstructured Hansard txt files into a structured database of speeches so that we can easily query the data by person, by date, et cetera. The idea is to convert each txt file into an array of JSON objects, where each object is a single "entry" from the transcript (e.g. a single speech, a header, ...) and each of these entries contains relevant data fields (e.g. name of the speaker, text of the speech, etc).


A better solution than this regex-based approach is to cast this as a supervised learning problem with three main steps: (a) classify each line as as either a "header", "speech", or "scene"; (b) for each speech, extract the speaker name from the first part of the line; (c) for each speaker name, parse it into three component parts: "title", "name", and "appointment".

If we can train a classifier to perform these steps well, then this will result in much less headache in the long-term.

Your task will be to construct a training set of hand-labeled lines for step (a) (and then we can more on to the other two steps). Here is a more detailed description of each of the three classification steps:

a. Classify each line of a txt file as either a "header", "speech", or "scene".

Each line in a transcript must be one of three basic types:

header: a document heading that provides structure in the document. Usually these are in all caps, but not always.

e.g. "WORKMEN'S COMPENSATION DUES—MR. NYATUGA"
e.g. "ORAL ANSWERS TO QUESTIONS"
e.g. "Question no. 136"
e.g. "First readings"
e.g. "Bills"
e.g. "THE BANKING (AMENDMENT) BILL"

speech: a speech consists of words spoken in the parliamentary debate.

e.g. "Mr. Mutiso: Sir, would the Assistant Minister tell "
e.g. "it was promised last year by hon. Khasakhala when "
e.g. "Mr. Deputy Speaker: Order It is now time for the 
Minister to reply."
e.g. "should be a law enforcing everybody who owns a piece "

scene: a line that provides the reader with context on what is happening, but is not part of a speech or a header. Usually this are within parentheses.
 
e.g. "(Applause)"
e.g. "(Orders for First Reading read the First Time Ordered to be read the Second Time today by leave of the House)"
e.g. "(Question put and agreed to)"
e.g. "(Several Members stood up)"
e.g. "The following papers were laid on the table:"
