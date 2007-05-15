#!/bin/bash

# checks revision in docs directory, updates entire local copy if needed,
# and generates the diff.

REPOS_PATH=http://code.djangoproject.com/svn/django/trunk/
LOCAL_PATH=/Users/ymasuda/work/django/trunk/
DOCJP_DIR=/Users/ymasuda/work/django/doc-jp/

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




