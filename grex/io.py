import json
import _jsonnet


def loadf(filename):
    if filename.endswith(".jsonnet"):
        return json.loads(_jsonnet.evaluate_file(filename))
    return json.loads(open(filename).read())

def render_string(string, **params):
    import jinja2
    env = jinja2.Environment()
    t = env.from_string(string)
    return t.render(**params)
