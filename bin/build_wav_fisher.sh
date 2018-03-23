#!/usr/bin/env bash
die () {
  echo >&2 "$@"
  exit 1
}
[ "$#" -eq 1 ] || die "Usage: $0 <LDC2010T04 directory>"
[ -d $1 ] || die "Could not find directory $1"
[ -d "$1/data/transcripts" ] || die "Directory $1 does not appear to be LDC2010T04"
BINDIR=`dirname $0`
TARGETDIR="`dirname $0`/../corpus/wav"

mkdir -p $TARGETDIR

for C in $(cd mapping; ls fisher*); do
  for F in $(cat mapping/$C | cut -d' ' -f1 | uniq); do
    echo "## FILE $F"
    cat $1/data/transcripts/$F.tdf |
    grep -v ";;MM" | grep -v "file;unicode" |
    cut -f 1-4
  done | $BINDIR/map_wav_fisher.py mapping/$C > $TARGETDIR/$C.es
done
