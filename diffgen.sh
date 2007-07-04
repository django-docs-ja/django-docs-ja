#!/bin/bash

# checks revision in docs directory, updates entire local copy if needed,
# and generates the diff.

REPOS_PATH=http://code.djangoproject.com/svn/django/branches/unicode
LOCAL_PATH=/Users/ymasuda/work/django/src/branches/unicode
DOCJP_DIR=/Users/ymasuda/work/django/unicode_merge/

# move clean up finished diffs to done directory
if [ ! -d $DOCJP_DIR/done ]; then
    mkdir $DOCJP_DIR/done;
fi

rm *.diff~
for i in $DOCJP_DIR/*.diff; do
    if [ "`head -n1 $i`" = "done." ]; then
	mv $i $DOCJP_DIR/zz_diff_done/
    fi
done

# find revision number.
LOCAL_REV=`svn info $LOCAL_PATH| awk "/Revision:/ { print \\$NF}"`
REPOS_REV=`svn info $REPOS_PATH| awk "/Revision:/ { print \\$NF}"`

# show current revision number, both for local copy and repository.
echo $LOCAL_REV in local copy, $REPOS_REV in repository.
if [ $LOCAL_REV -lt $REPOS_REV ]; then
    # remote repository has upadted.
    pushd $LOCAL_PATH; svn update;
    svn diff $LOCAL_PATH/docs -r$LOCAL_REV:$REPOS_REV > $DOCJP_DIR/to_$REPOS_REV.diff
    echo Local copy updated to $REPOS_REV.
    popd
else
    echo 'Local copy is up to date.'
fi




