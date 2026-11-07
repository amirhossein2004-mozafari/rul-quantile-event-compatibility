# Obtain NASA data separately

NASA raw data, including the official RUL label text files, are not redistributed. Obtain C-MAPSS FD001-FD004 from NASA's Prognostics Center of Excellence data repository. Use the N-CMAPSS dataset entry for N-CMAPSS DS01-005 if reproducing the descriptive external-data check.

https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/

The historical scripts expect extracted C-MAPSS files under data/raw/cmapss/ and N-CMAPSS under data/raw/ncmapss/. NASA_EXPECTED_SHA256.csv records known hashes of the local extracted files examined in the project. These hashes do not establish NASA certification. Different line endings change hashes.

The 2,873,351,432-byte N-CMAPSS HDF5 and the 437,916,817-byte partial download are excluded. The partial file is not a complete dataset.

Public arithmetic checks use saved prediction labels for consistency. They cannot independently compare those labels with excluded NASA files.
