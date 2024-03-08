# Mapset Statistician

## About
  Mapset Statistician is a modding tool for osu!mania that allows the user to graph certain characteristics of difficulties in a mapset next to each other for comparison.
  This application is **NOT** a problem detector. It's meant to provide general diagnostic information about the difficulties in a mapset to aid the modder in finding issues.
  Please read the documentation. There are sliders and options whose functions aren't immediately clear. The documentation explains them.
  This application is still in dev. There is no executable available for the end-user yet. A first version will be released soon.

## Documentation (WIP)

### Basic Graph Functionality
  Every hit object (or LN release, depending on what's being graphed) is algorithmically assigned a strain value depending on the graph type and parameters in the control panel. The strain is then graphed against time as "strain per second," averaged over a time window of `±S`, where `S` corresponds to the value for the `Smoothing` slider.

  For graph types labelled with `Balance`, what's being graphed is the ratio of the "strains" being compared (e.g. left vs. right hand or rice vs. LN), mapped onto a range of `[-1,1]` using the function `y(ratio) = 1 - (2 / (ratio + 1))`.

### Absolute/RC/LN Density

### Absolute/RC/LN Hand Balance

### RC/LN Balance

### Jack Intensity

### Jack Balance

### Asynchronous Releases
