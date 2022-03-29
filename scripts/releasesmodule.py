import utilsmodule as um

releases = {
    "v1.0.0": {
        "title": "First release",
        "type": "Beta",
        "date": "2022-03-29",
        "url": {
            "win64": "https://bit.ly/3x1ryMP",
            "macos": "https://bit.ly/36GHJEa"
        },
        "changelog": [
            """First version of the Demo, allowing to classify point-clouds with pre-trained networks. 
Point clouds are loaded from ply files with oriented normals (fields nx, ny, nz)."""
        ]
    }
}


release_article_template = """
            <article>
              <h2>@rtitle@</h2>
              <ul>
                 <li><b>Release version</b>: @rversion@</li>
                 <li><b>Release date</b>: @rdate@</li>
                 <li><b>Release type</b>: @rtype@</li>
                 <li><b>Changelog</b>: @rchangelog@</li>
                 <li><b>Download links</b>: @rlinks@</li>
              </ul>
            </article>
"""


def build_release_list():
    rlist = ""

    for v, r in releases.items():
        # build download link list
        rurl = "<ul>" + \
               ' '.join(['<li><b>{key}</b>: <a href="{value}">{value}</a></li>'.format(key=k, value=i) for k,i in r["url"].items()]) + \
               "</ul>"

        pstring='<p style="text-align: justify; margin-bottom:0px;">'

        rep = {
            "@rversion@": v,
            "@rtitle@": r["title"],
            "@rdate@": r["date"],
            "@rtype@": r["type"],
            "@rlinks@": rurl,
            "@rchangelog@": pstring + ('</p>'+pstring).join(r["changelog"]) + '</p>'
        }
        rlist = rlist + um.processWildcards(release_article_template, rep)

    return rlist
