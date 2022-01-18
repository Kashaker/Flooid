from eot.wowool.error import Error
from eot.wowool.native import Analyzer, Domain, LanguageIdentifier
from eot.wowool.annotation import Concept
from eot.io.input_providers import InputProviders
from eot.io.input_provider_html import HTMLFileInputProvider
from eot.wowool.native_tool.entity_graph import EntityGraph
from eot.wowool.native_tool.entity_graph.cypher import CypherStream
import wowool

import pandas as pd
import argparse
import traceback
from pathlib import Path


try:
    import neo4j
except ModuleNotFoundError as ex:
    print(f"{ex}, to install: pip install neo4j-connector ")
    exit(-1)


graph_config = {

    "slots" : { "Doc" : { "format" : "{Path(document.document_id).parts[-2]}" } },
    "links" :[
    {
        "from"      : { "slot" : "Doc" },
        "to"        : { "expr":"HR" },
        "relation"  : { "label": "subject" }
    },
    {
        "from"      : { "slot" : "Doc" },
        "to"        : { "expr":"City" },
        "relation"  : { "label": "Located in" }
    },
    {
        "from"      : { "slot" : "Doc" },
        "to"        : { "expr":"EducationType" },
        "relation"  : { "label": "Type" }
    },
    {
        "from"      : { "slot" : "Doc" },
        "to"        : { "expr":"University_Projects" },
        "relation"  : { "label": "Projects" }
    },
    {
        "from"      : { "slot" : "Doc" },
        "to"        : { "expr":"POBox" },
        "relation"  : { "label": "P.O. Box" }
    },
    {
        "from"        : { "expr":"Person" },
        "to"      : { "slot" : "Doc" },
        "relation"  : { "label": "linked_to" }
    },
    {
        "from"        : { "expr":"Person" },
        "to"      : { "expr" : "Position" },
        "relation"  : { "label": "works_as" }
    },
    {
        "from"        : { "expr":"Person" },
        "to"      : { "expr" : "FocusCompany" },
        "relation"  : { "label": "company" }
    },
    {
        "to"      : { "expr" : "University_Projects" },
        "from"        : { "expr":"Topics", "content" : "{eot.string.initial_caps(stem)}" },
        "relation"  : { "label": "Topic" }
    },
    {
        "from"      : { "slot" : "Doc" },
        "to"        : { "expr":"Address" },
        "relation"  : { "label": "Address" }
    },
    {
        "from"      : { "slot" : "Doc" },
        "to"        : { "expr":"TelephoneNumber" },
        "relation"  : { "label": "Telephone" }
    },
    {
        "from"      : { "slot" : "Doc" },
        "to"        : { "expr":"Email" },
        "relation"  : { "label": "Email" }
    },
    {
        "from"      : { "slot" : "Doc" },
        "to"        : { "expr":"Partner" },
        "relation"  : { "label": "linked_to" }
    },
    {
        "from"      : { "slot" : "Doc" },
        "to"        : { "expr":"Technology" },
        "relation"  : { "label": "Uses" }
    },
    {
        "from"      : { "slot" : "Doc" },
        "to"        : { "expr":"Education" },
        "relation"  : { "label": "subject" }
    },
    {
        "from"      : { "slot" : "Doc" },
        "to"        : { "expr":"Innovation" },
        "relation"  : { "label": "subject" }
    },
    {
        "from"      : { "slot" : "Doc" },
        "to"        : { "expr":"Health" },
        "relation"  : { "label": "subject" }
    },
    {
        "from"      : { "slot" : "Doc" },
        "to"        : { "expr":"ITC" },
        "relation"  : { "label": "subject" }
    }
    ]
}




def parse_arguments():
    """
    Parses the command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f" , "--file", help="files")
    parser.add_argument("--format", help="file format, html or txt", default="txt")
    parser.add_argument("-d" , "--domain", help="domain", default="rules")
    parser.add_argument("-s", "--server", help="server connection", default="http://host.docker.internal:7474")
    parser.add_argument("-u", "--user", help="user name", default="test")
    parser.add_argument("-p", "--password", help="password for the given connection", default="test")
    args = parser.parse_args()
    return args

args = parse_arguments()

mydomain=Domain(args.domain)


corpus = InputProviders(args.file)
lid = LanguageIdentifier()
graphit = EntityGraph(graph_config)

neo4jdb = neo4j.Connector(args.server, (args.user, args.password))

try:

    cs = CypherStream("EOT")
    #entities = Domain(f"{language}-entity")
    entities = {}
    analyzers = {}

    for ip in corpus:
        print(ip.id())
        text_data = ip.text()

        language = lid(text_data)

        if language not in entities:
            analyzers[language] = Analyzer(language=language)
            entities[language] = Domain(f"{language}-entity")
        doc = entities[language](analyzers[language](ip))
        doc = mydomain(doc)
        #print(doc)
        # returns a panda dataframe.
        # graphit.slots["Document"] = {"data": "hello"}
        results = graphit(doc)

        print(results.df_from)
        print(results.df_relation)
        print(results.df_to)
        res = results.merge()
        print(res)
        for neo4j_query in cs(results):
            print(neo4j_query)
            neo4jdb.run(neo4j_query)


except Exception as ex :
    traceback.print_exc()
    print("Something went wrong !!!", ex)
#             print_subclass = ', '.join(current_subclass)
