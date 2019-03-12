file(REMOVE_RECURSE
  "../../../../lib/libcarotene.pdb"
  "../../../../lib/libcarotene.a"
)

# Per-language clean rules from dependency scanning.
foreach(lang CXX)
  include(CMakeFiles/carotene.dir/cmake_clean_${lang}.cmake OPTIONAL)
endforeach()
