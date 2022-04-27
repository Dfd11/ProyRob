#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/dfd/ProyRob/src/roboclaw_node"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/dfd/ProyRob/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/dfd/ProyRob/install/lib/python2.7/dist-packages:/home/dfd/ProyRob/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/dfd/ProyRob/build" \
    "/usr/bin/python2" \
    "/home/dfd/ProyRob/src/roboclaw_node/setup.py" \
     \
    build --build-base "/home/dfd/ProyRob/build/roboclaw_node" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/dfd/ProyRob/install" --install-scripts="/home/dfd/ProyRob/install/bin"
