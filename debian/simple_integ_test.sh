#!/bin/bash
set -eu
echo "Expect 'OK' on success"
fn=/tmp/xattr.test
rm -f $fn
touch $fn
[[ $(xattr -p user.foo $fn 2>&1 ) == "No such xattr: user.foo" ]]
xattr -w user.foo bar $fn
[[ $(xattr -p user.foo $fn) == "bar" ]]
[[ $(xattr $fn) == "user.foo" ]]
xattr -d user.foo $fn
[[ $(xattr $fn) == "" ]]
[[ $(xattr -p user.foo $fn 2>&1 ) == "No such xattr: user.foo" ]]
echo OK
