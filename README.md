# Spread Wizard

## About
  Spread Wizard is a modding tool for osu!mania that allows the user to graph certain characteristics of difficulties in a mapset next to each other for comparison.
  This application is **NOT** a problem detector. It's meant to provide general diagnostic information about the difficulties in a mapset to aid the modder in finding issues.
  Please read the documentation. There are sliders and options whose functions aren't immediately clear. The documentation explains them.

## Documentation (WIP)

### Basic Graph Functionality
  Every hit object (or LN release, depending on what's being graphed) is algorithmically assigned a strain value depending on the graph type and parameters in the control panel. The strain is then graphed against time as "strain per second," averaged over a time window of `±S`, where `S` corresponds to the value for the `Smoothing` slider.

  For graph types labelled with `Balance`, what's being graphed is the ratio of the "strains" being compared (e.g. left vs. right hand or rice vs. LN), mapped onto a range of `[-1,1]` using the function `y(ratio) = 1 - (2 / (ratio + 1))`.

### Absolute/RC/LN Density
  Every note is assigned a strain of 1. The strains are summed over a window of `±Smoothing` at each timestamp, then averaged over time to give `strain per second`, which is just `notes per second` in this case.
  The RC/LN Density options do the exact same thing as Absolute density, but only counts rice notes or long notes, respectively.

### Absolute/RC/LN Hand Balance
  Notes per second is calculated on each hand exactly as above, with the middle key in odd keymodes counting twice, once for each hand. The ratio of `Right strain:Left strain` is taken and transformed to fit in the range `[-1,1]`, such that:
    - `1` and `-1` correnpond to 100% right and left hand loading, respectively.
    - `0` corresponds to equal note density across both hands.
    - `.2`, `.5` correnponds to and 60% and 75% right hand loading, respectively.
    - etc

### RC/LN Balance
  The same calculation from the `Hand Balance` graphs are used, except the ratio of interest is `Rice density:LN density` rather than `Right hand:Left hand`

### Jack Intensity
  If **Alternate Calculator** is not checked:
    Every note is assigned a strain of 1 if the distance between that note and the previous note in the same column is less than `Max. Stack Distance`, else a strain of 0. The `strain per second` is then calculated and plotted as in the `Density` graphs.
    Adjusting the `Max. Stack Distance` would be useful for finding unwanted jacks at a certain tightness.
  If **Alternate Calculator is checked:
    Every note is assigned a strain that scales with the inverse square of the distance from the previous note in the same column such that at 180BPM, 1/4, 1/2, and 1/1 stacks have strains of 4, 1 and .25, respectively. The `strain per second` is then calculated and plotted as in     the `Density` graphs.

### Jack Balance

### Asynchronous Releases
