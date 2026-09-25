#!/bin/sh
# M5-R input materialisation (WORKER-2 lane).
#
# Reads (READ-ONLY) the ended worker lane arena/01a0d581-fleetyard for the
# inherited M5 raw census + fixtures, and reproduces the frozen corpus from the
# sha-verified zip. Nothing here writes to any other branch.
#
#   sh tools/m5r_inputs.sh [evidence-dir]   (default: evidence)
#
# Outputs (working evidence; never committed):
#   evidence/runs/m5-raw/records/*.json   1334 raw signals (230 files)
#   evidence/fixtures/…                   confirmed/clean/negative fixtures
#   corpus/…                              corpus/docdocgo/overlays/*.txt (230)
set -eu

E="${1:-evidence}"
ARCHIVE_REF="refs/heads/arena/01a0d581-fleetyard"
ARCHIVE_LOCAL="refs/remotes/origin/arena/01a0d581-fleetyard"
ZIP_SHA_PREFIX="3f36c5203910"

git fetch origin "$ARCHIVE_REF:$ARCHIVE_LOCAL"
mkdir -p "$E"
git archive "$ARCHIVE_LOCAL" runs/m5-raw fixtures | tar -x -C "$E"

mkdir -p corpus
unzip -q -o docdocgo-fixes.zip -d corpus/

ZIP_SHA=$(sha256sum docdocgo-fixes.zip | cut -d' ' -f1)
case "$ZIP_SHA" in
  "$ZIP_SHA_PREFIX"*) ;;
  *) echo "FATAL: corpus zip sha256 $ZIP_SHA does not start $ZIP_SHA_PREFIX" >&2; exit 1;;
esac
echo "corpus zip ok ($ZIP_SHA_PREFIX…); transcripts: $(ls corpus/docdocgo/overlays/*.txt | wc -l)"
echo "records: $(ls "$E"/runs/m5-raw/records/*.json | wc -l) files"
echo "inputs ready under $E/ and corpus/"
