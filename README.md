# Spread Wizard

## About
  Spread Wizard is a modding tool for osu!mania that allows the user to graph certain characteristics of difficulties in a mapset next to each other for comparison.
  This application is **NOT** a problem detector. It's meant to provide general diagnostic information about the difficulties in a mapset to aid the modder in finding issues.
  Please read the documentation. There are sliders and options whose functions aren't immediately clear. The documentation explains them.

## Documentation

### Basic Graph Functionality
Every hit object (or LN release, depending on what's being graphed) is algorithmically assigned a strain value depending on the graph type and parameters in the control panel. The strain is then graphed against time as "strain per second," averaged over a time window of `±Smoothing`

For graph types labelled with `Balance`, what's being graphed is the ratio of the "strains" being compared (e.g. left vs. right hand or rice vs. LN), mapped onto a range of `[-1,1]` using the function `y(ratio) = 1 - (2 / (ratio + 1))`.

### Absolute/RC/LN Density
Every note is assigned a strain of 1. The strains are summed over a window of `±Smoothing` at each timestamp, then averaged over time to give `strain per second`, which is just `notes per second` in this case.
The `RC/LN Density` options do the exact same thing as `Absolute Density`, but only counts rice notes or long notes, respectively.

### Absolute/RC/LN Hand Balance
Notes per second is calculated on each hand exactly as above, with the middle key in odd keymodes counting twice, once for each hand. The ratio of `Right strain:Left strain` is taken and transformed to fit in the range `[-1,1]`, such that:
  - `1` and `-1` correspond to 100% right and left hand loading, respectively.
  - `0` corresponds to equal note density across both hands.
  - `.2` and `.5` corresponds to and 60% and 75% right hand loading, respectively.
  - etc.

### RC/LN Balance
The same calculation from the `Hand Balance` graphs are used, except the ratio of interest is `Rice density:LN density` rather than `Right hand:Left hand`

### Jack Intensity
If **Alternate Calculator** is not checked:
Every note is assigned a strain of 1 if the distance between that note and the previous note in the same column is less than `Max. Stack Distance`, else a strain of 0. The `strain per second` is then calculated and plotted as in the `Density` graphs.
Adjusting the `Max. Stack Distance` would be useful for finding unwanted jacks at a certain tightness.
  
If **Alternate Calculator** is checked:
Every note is assigned a strain that scales with the inverse square of the distance from the previous note in the same column such that at 180BPM, 1/4, 1/2, and 1/1 stacks have strains of 4, 1 and .25, respectively. The `strain per second` is then calculated and plotted as in the `Density` graphs.

### Jack Balance
Plots the hand balance, but using the strains calculated from `Jack Intensity` rather than from `Density`.

### Asynchronous Releases
All LN releases are assigned a strain equal to the number of other LNs being held at the time of release. The `strain per second` is then calculated and plotted as in the `Density` graphs.
  - All LNs shorter than `Min. LN Length` are not considered in calculations. Set this value to `0` unless you want to control for short "rice LNs".
  - If an LN release is less than `Overlap Tolerance` later than a concurrent LN's head or before a concurrent LN's tail, it is not considered an asynchronous release. Set this value to `0` unless you want to control for LN graces.
  - This graphing option is very poorly optimized. Please be ready to wait a couple seconds every time you select a difficulty or move a slider.

