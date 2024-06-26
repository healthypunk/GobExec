from pathlib import Path

import gobexec.main
from gobexec.goblint.bench import txtindex
from gobexec.goblint.result import AssertTypeSummary
from gobexec.goblint.tool import GoblintTool

from gobexec.model.result import TimeResult
from gobexec.model.tools import ExtractTool
from gobexec.output.renderer import FileRenderer, ConsoleRenderer, MultiRenderer

goblint_assert = GoblintTool(
    name="goblint_assert",
    program=str(Path("../analyzer/goblint").absolute()),
    args=["-v", "--conf", str(Path("../analyzer/conf/traces-rel.json").absolute()), "--enable", "warn.debug","--set", "trans.activated[+]", "assert",
          "--set" ,"ana.activated[+]" ,"apron" ,"--set" ,"ana.path_sens[+]" ,"threadflag", "--set" ,"ana.relation.privatization", "mutex-meet-tid-cluster12"],
    dump = "assert"
)

def index_tool_factory(name, args):
    goblint = GoblintTool(
        name=name,
        program=str(Path("../analyzer/goblint").absolute()),
        args=["-v", "--conf", str(Path("../analyzer/conf/traces-rel.json").absolute()), "--enable", "warn.debug"] + args,
        dump= 'apron',
        assertion = goblint_assert
    )

    return ExtractTool(
        goblint,
        TimeResult,
        AssertTypeSummary,

    )

matrix = txtindex.load(Path("../bench/index/traces-rel-yaml.txt").absolute(),index_tool_factory)
matrix.tools.insert(0,ExtractTool(goblint_assert))
html_renderer = FileRenderer(Path("out.html"))
console_renderer = ConsoleRenderer()
renderer = MultiRenderer([html_renderer, console_renderer])

gobexec.main.run(matrix, renderer)