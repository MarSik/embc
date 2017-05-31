# CMake configuration for {{ name }}
FUNCTION(USE_{{ name }} PROJECT)
FIND_OR_DOWNLOAD("{{ name }}" "{{ url }}" "{{ name }}.{{ format }}")
SET_PROPERTY(TARGET ${PROJECT} APPEND PROPERTY INCLUDE_DIRECTORIES "${PROJECT_SOURCE_DIR}/lib/{{ name }}")
FILE(GLOB_RECURSE FOUND
     "${PROJECT_SOURCE_DIR}/lib/{{ name }}/src/*.[cCsShH]"
     "${PROJECT_SOURCE_DIR}/lib/{{ name }}/src/*.[cCsShH][pP][pP]")
SET_PROPERTY(TARGET ${PROJECT} APPEND PROPERTY SOURCES ${FOUND})
ENDFUNCTION(USE_{{ name }} PROJECT)
