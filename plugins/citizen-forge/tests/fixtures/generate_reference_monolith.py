def reference_monolith() -> str:
    lines = [
        "<!doctype html>",
        "<script>",
        "const DATA = '" + ("x" * 2048) + "';",
        "window.onload = () => document.write(DATA);",
        "function save(){ open(__file__, 'w'); }",
        "function patch(){ document.documentElement.innerHTML = DATA; }",
    ]
    lines.extend("// last-write-wins filler {}".format(index) for index in range(4993))
    lines.append("</script>")
    return "\n".join(lines)
