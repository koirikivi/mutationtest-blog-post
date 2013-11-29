#!/bin/bash
cat _header.html > blogiposti.html \
    && markdown blogiposti.markdown >> blogiposti.html \
    && echo "</body></html>" >> blogiposti.html
