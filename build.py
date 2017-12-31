#!/usr/bin/env python3
# -*- coding: utf8 -*-

#####################################################################################
#              CoCalc Examples - Documentation Files Compiler                       #
#                                                                                   #
#                Copyright (C) 2015 -- 2017, SageMath, Inc.                         #
#                                                                                   #
#  Distributed under the terms of the GNU General Public License (GPL), version 2+  #
#                                                                                   #
#                        http://www.gnu.org/licenses/                               #
#####################################################################################

import os, sys

# make it python 2 and 3 compatible (although, to be clear, it is supposed to be py3 only)
if (sys.version_info > (3, 0)):
    mystr = str
else:
    mystr = basestring

from os.path import abspath, dirname, normpath, exists, join
from os import makedirs, walk
from shutil import rmtree
import yaml
import json
import re
from codecs import open
from collections import defaultdict
from pprint import pprint

""" # TODO enable hashtags later
hashtag_re = re.compile(r'#([a-zA-Z].+?\b)')
def process_hashtags(match):
    ht = match.group(1)
    return "<a class='webapp-examples-hashtag' href='{0}'>#{0}</a>".format(ht)
"""

def process_category(doc):
    '''
    Preprocess the 2-level categories for an entry. Either a list/tuple or string with a common "/" slash.
    '''
    cats = doc["category"]
    if isinstance(cats, (list, tuple)):
        assert len(cats) == 2
    elif isinstance(cats, mystr):
        cats = cats.split("/", 1)
    else:
        raise AssertionError("Supposed category '{}' cannot be processed".format(cats))
    sortweight = float(doc.get("sortweight", 0.0))
    lvl1, lvl2 = [c.strip().title() for c in cats]
    return lvl1, lvl2, sortweight

def process_doc(doc, input_fn):
    """
    This processes one document entry and returns the suitable datastructure for later conversion to JSON.
    """
    #if not all(_ in doc.keys() for _ in ["title", "code", "descr"]):
    #    raise AssertionError("keyword missing in %s in %s" % (doc, input_fn))
    title       = doc["title"].strip()
    code        = doc["code"].strip()
    if 'descr' in doc:
        description = doc["descr"].strip() # hashtag_re.sub(process_hashtags, doc["descr"])
    else:
        description = title
    body        = [code, description]
    # attribution
    if "attr" in doc:
        body.append(doc["attr"])
    return title, body

def examples_data(input_dir, output_fn):
    input_dir     = abspath(normpath(input_dir))
    examples_json = abspath(normpath(output_fn))
    output_dir    = dirname(examples_json)
    print("Target output directory: '{}'".format(output_dir))

    # this implicitly defines all known languages
    recursive_dict = lambda : defaultdict(recursive_dict)
    examples = {
        "sage":   recursive_dict(),
        "python": recursive_dict(),
        "r":      recursive_dict(),
        "cython": recursive_dict(),
        "gap":    recursive_dict(),
        "bash":   recursive_dict(),
        "octave": recursive_dict(),
    }

    # This processes all yamk input files and fails when any assertion is violated.
    for root, _, files in walk(input_dir):
        for fn in filter(lambda _ : _.lower().endswith("yaml"), files):
            input_fn = join(root, fn)
            data = yaml.load_all(open(input_fn, "r", "utf8").read())

            language = entries = lvl1 = lvl2 = titles = sortweight = None # will be set in the "category" case, which comes first!

            for doc in data:
                if doc is None:
                    continue

                processed = False

                if "language" in doc:
                    language = doc["language"]
                    if language not in examples.keys():
                        raise AssertionError("Language %s not known. Fix first document in %s" % (language, input_fn))
                    processed = True

                if "category" in doc: # setting both levels of the category and re-setting entries and titles
                    lvl1, lvl2, sortweight = process_category(doc)
                    if lvl2 in examples[language][lvl1]:
                        raise AssertionError("Duplicate category level2: '%s' already exists (error in %s)" % (lvl2, input_fn))
                    entries = []
                    examples[language][lvl1][lvl2] = {'entries': entries, 'sortweight': sortweight}
                    titles = set()
                    processed = True

                if all(_ in doc.keys() for _ in ["title", "code"]):
                    # we have an actual document entry, append it in the original ordering as a tuple.
                    try:
                        title, body = process_doc(doc, input_fn)
                    except Exception as ex:
                        print("Problem processing {language}::{lvl1}/{lvl2} of {input_fn}".format(**locals()))
                        raise ex
                    if title in titles:
                        raise AssertionError("Duplicate title '{title}' in {language}::{lvl1}/{lvl2} of {input_fn}".format(**locals()))
                    entry = [title, body]
                    entries.append(entry)
                    titles.add(title)
                    processed = True

                # if False, malformatted document
                if not processed: # bad document
                    raise RuntimeError("This document is not well formatted (wrong keys, etc.)\n%s" % doc)

    if not os.path.exists(output_dir):
        print("Creating output directory '%s'" % output_dir)
        os.makedirs(output_dir)

    with open(examples_json, "w", "utf8") as f_out:
        # sorted keys to de-randomize output (leads to a stable representation when kept it in Git)
        json.dump(examples, f_out, ensure_ascii=True, sort_keys=True, indent=1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: %s <input-directory of *.yaml files> <ouput-file (usually 'examples.json')>" % sys.argv[0])
        sys.exit(1)
    examples_data(sys.argv[1], sys.argv[2])

