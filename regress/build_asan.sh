#!/bin/bash
# Build the AddressSanitizer/UBSan binaries that gate 9 needs.
#
#   ./build_asan.sh          both HEAD and pristine (the three-way)
#   ./build_asan.sh head     HEAD only
#
# Two binaries, because gate 9's assertion is DIRECTIONAL: a machine clean under upstream
# and dirty under HEAD is a regression, while dirty-upstream/clean-HEAD is the fork doing
# its job. Without the pristine build the gate can only report, not compare.
#
# TWO BUILD NOTES, both learned by getting them wrong:
#
#  * do NOT add -fno-sanitize-recover=address. With it, the build dies generating
#    src/include/ppc_spr_strings.h: the header generators are host tools compiled with the
#    same CFLAGS, and the generating rule is a pipeline whose exit status is the tool's, so
#    a non-recoverable sanitizer hit inside a build tool fails the whole build with a bare
#    "Error 1" on a header that is fine. Leaving recovery on builds cleanly.
#  * detect_leaks=0 during the build and the sweep. The emulator is killed mid-run, so
#    exit-time leaks are expected and say nothing. ASan's memory-error detection is
#    unaffected -- and this matches what the project did before ("only benign exit-time
#    LeakSanitizer leaks", CHANGELOG).
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
SEC=$(cd "$HERE/.." && pwd)
WHICH=${1:-both}

export ASAN_OPTIONS=detect_leaks=0

build_one() {   # ref, dir, label
    local src=$1 dir=$2 lab=$3
    echo "######## $lab -> $dir ########"
    rm -rf "$dir"; mkdir -p "$dir"
    ( cd "$SEC" && git archive "$src" ) | tar -x -C "$dir"
    # the repo does not track the exec bit; without this, configure fails rc=126
    chmod +x "$dir/configure" 2>/dev/null
    find "$dir" -name '*.sh' -exec chmod +x {} + 2>/dev/null
    cd "$dir" || return 1
    export CFLAGS="-O1 -g -fno-omit-frame-pointer -fsanitize=address,undefined"
    export LDFLAGS="-fsanitize=address,undefined"
    sh ./configure > configure.log 2>&1
    make -j12 > build.log 2>&1
    echo "  make rc=$?  objs=$(find src -name '*.o' | wc -l)"
    if [ -x gxemul ]; then
        echo "  binary: $(stat -c%s gxemul) bytes"
    else
        echo "  BUILD FAILED:"
        grep -E "Error [0-9]+|error:" build.log | head -8 | sed 's/^/    /'
        return 1
    fi
}

case "$WHICH" in
    head) build_one HEAD /tmp/gx-asan-head head ;;
    *)    build_one HEAD /tmp/gx-asan-head head
          echo
          build_one 39748e3 /tmp/gx-asan-pristine pristine ;;
esac
echo "BUILD_ASAN_DONE"
