#Extracts filenames and line numbers from git diff
#Currently configured to compare against HEAD~
#Can be used standalone or with wrapper.sh
#Reference: John Mellor on Stack Overflow, 2012
#https://stackoverflow.com/questions/8259851/using-git-diff-how-can-i-get-added-and-modified-lines-numbers

diff-lines() {
    local path=
    local line=
    while read; do
        esc=$'\033'
        if [[ $REPLY =~ ---\ (a/)?.* ]]; then
            continue
        elif [[ $REPLY =~ \+\+\+\ (b/)?([^[:blank:]$esc]+).* ]]; then
            path=${BASH_REMATCH[2]}
        elif [[ $REPLY =~ @@\ -[0-9]+(,[0-9]+)?\ \+([0-9]+)(,[0-9]+)?\ @@.* ]]; then
            line=${BASH_REMATCH[2]}
        elif [[ $REPLY =~ ^($esc\[[0-9;]+m)*([\ +-]) ]]; then
            echo "$path:$line:$REPLY"
            if [[ ${BASH_REMATCH[2]} != - ]]; then
                ((line++))
            fi
        fi
    done
}

#git diff -U0 HEAD~ | diff-lines | sed "s/^/\"/ ; s/:/\" \"/" | sed "s/:.*/\"/g"
#That was an attempt to protect for spaces in filenames
git diff -U0 HEAD~ | diff-lines | sed "s/:/ /" | sed "s/:.*//g"
