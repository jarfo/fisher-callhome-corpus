#!/usr/bin/env bash
die () {
  echo >&2 "$@"
  exit 1
}
[ "$#" -eq 1 ] || die "Usage: $0 <LDC96T17 directory>"
[ -d $1 ] || die "Could not find directory $1"
[ -d "$1/transcrp" ] || die "Directory $1 does not appear to be LDC96T17"
BINDIR=`dirname $0`
TARGETDIR="`dirname $0`/../corpus/wav"

mkdir -p $TARGETDIR

for C in $(cd mapping; ls callhome*); do
  for F in $(cat mapping/$C | cut -d' ' -f1 | uniq); do
    echo "## FILE $F"
    cat $1/transcrp/*/$F.txt |
    iconv -f iso8859-1 -t utf8 |
    sed -e 's/^ *//' |
    cut -f 1-3 -d ' '
  done | $BINDIR/map_wav_callhome.py mapping/$C > $TARGETDIR/$C.es
done
