for f in *.jpg ; do
  if [[ $(file -b --mime-type "$f") = image/png ]] ; then
    mv "$f" "${f/%.png/.jpg}"
  fi
done
