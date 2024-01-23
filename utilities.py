

DB_CONNECTION = "__db__connection__"
CUSTOM_CODE_BEGIN = "-- Begin Custom Python Code --"
CUSTOM_CODE_END = "-- End Custom Python Code --"
STRUCTURE_BEGIN = "-- Begin Structure --"
STRUCTURE_END = "-- End Structure --"
INSERT_BEGIN = "-- Begin Inserts --"
INSERT_END = "-- End Inserts --"


def split_schema(schema_file: str):
    f = open(schema_file, "r")
    contents = f.read()
    f.close()

    structure = ""
    inserts = ""
    custom_code = ""

    if contents.find(INSERT_BEGIN) != -1 and contents.find(INSERT_END) != -1:
            inserts = contents.split(INSERT_BEGIN)[1].split(INSERT_END)[0]

    if contents.find(CUSTOM_CODE_BEGIN) != -1 and contents.find(CUSTOM_CODE_END) != -1:
            custom_code = contents.split(CUSTOM_CODE_BEGIN)[1].split(CUSTOM_CODE_END)[0]

    if contents.find(STRUCTURE_BEGIN) != -1 and contents.find(STRUCTURE_END) != -1:
            structure = contents.split(STRUCTURE_BEGIN)[1].split(STRUCTURE_END)[0]

    return (structure, inserts, custom_code)

def execute_python_code(script, connection):
    if len(script) != 0:
        env = {DB_CONNECTION: connection}
        exec(script, env)